"""只读抓取官方文档及指定版本源码，留存核查快照，不执行网页内容。"""
import concurrent.futures
import hashlib
import json
import re
import sys
import urllib.request
from html import unescape
from pathlib import Path

BASE = Path(__file__).resolve().parent
manifest_path = BASE / "外部来源核查.json"
items = json.loads(manifest_path.read_text(encoding="utf-8"))
all_items = items
if "--retry-failed" in sys.argv:
    items = [item for item in items if item.get("http_status") != 200]
targets = {
    "O6": "https://raw.githubusercontent.com/open-mmlab/mmdetection/v3.3.0/configs/_base_/models/retinanet_r50_fpn.py",
    "O7": "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/utils/metrics.py",
    "O8": "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/engine/trainer.py",
    "O9": "https://raw.githubusercontent.com/cocodataset/cocoapi/master/PythonAPI/pycocotools/cocoeval.py",
    "O10": "https://ar5iv.labs.arxiv.org/html/1708.02002",
}
patterns = {
    "O1": ["YOLO11s", "YOLO11l"],
    "O2": ['split', 'NMS', 'conf'],
    "O3": ['resume', 'batch', 'optimizer'],
    "O4": ['num_classes', 'categories'],
    "O5": ['tools/test.py', 'checkpoint'],
    "O6": ['FocalLoss', 'max_per_img', 'nms'],
    "O7": ['def fitness', 'w = [0.0', 'f1.mean', 'argmax'],
    "O8": ['best_fitness == self.fitness', 'best_fitness < fitness'],
    "O9": ['self.iouThrs', 'self.maxDets'],
    "O10": ['Focal Loss', 'RetinaNet', 'easy', 'modulating'],
}
review_notes = {
    "O1": "模型表明确列出yolo11s.pt与yolo11l.pt，支持Detection的训练、验证、推理和导出。未将其官方COCO数值复制为本项目成绩。",
    "O2": "Arguments中split可取val/test/train；iou解释为NMS阈值；conf是预测最低分数；当前文档说明汇总P/R取max-F1工作点。当前默认值及新增功能不反推历史run。",
    "O3": "训练指南列出batch与优化器等参数，并说明resume可恢复已有训练状态。本项目实际args与完整中断条件仍需历史文件。",
    "O4": "自定义数据指南要求metainfo中的classes、标注categories和num_classes一致；category_id须有效。指南说明可将非连续类别ID映射到连续标签。",
    "O5": "官方测试接口接受CONFIG_FILE与CHECKPOINT_FILE，示例使用tools/test.py；实际评估划分由配置决定，命令名不证明测试独立性。",
    "O6": "指定版本基础配置的backbone.depth=50、neck.type=FPN、loss_cls.type=FocalLoss；test_cfg包含score_thr=0.05、NMS阈值0.5及max_per_img=100。它不是项目已核对的有效配置。",
    "O7": "raw第1009–1012行Metric.fitness采用权重[0,0,0,1]，只用mAP50–95；第885–886行用平滑平均F1曲线的最大位置读取P/R。代码tag不证明历史安装文件未被修改。",
    "O8": "raw第712–714行在best_fitness与本轮fitness相等时写best.pt；第814–817行从指标取fitness并更新最佳值。不能据此直接认定具体历史checkpoint epoch。",
    "O9": "Params.setDetParams使用IoU 0.50至0.95、步长0.05；recall采样0至1；默认maxDets为1、10、100。项目是否覆盖默认值仍待有效配置。",
    "O10": "核查原论文ar5iv HTML呈现的§3.2、式(5)与§4：带alpha权重的Focal Loss降低易样本贡献；RetinaNet由ResNet/FPN及分类、框回归子网络构成。通用检测论文不证明本项目牛只性能。",
}
(BASE / "官方核查快照").mkdir(exist_ok=True)

if "--finalize-reviewed" in sys.argv:
    for item in all_items:
        assert item.get("http_status") == 200, item["id"]
        item["status"] = "相关正文与指定版本源码已核对"
        item.pop("error", None)
        if item["id"] == "O7":
            item["locator"] = "Metric.fitness L1009–1012；ap_per_class L885–886"
        elif item["id"] == "O8":
            item["locator"] = "save_model L712–714；validate L814–817"
        note = ("核查摘记（非网页或论文全文）\n"
                f"来源：{item['title']}\n"
                f"原始URL：{item['url']}\n"
                f"本次读取URL：{item['resolved_url']}\n"
                f"核查日期：{item['checked']}\n"
                f"下载内容SHA-256：{item['sha256_download']}\n"
                f"定位：{item['locator']}\n"
                f"摘记：{review_notes[item['id']]}\n")
        (BASE / item["snapshot"]).write_text(note, encoding="utf-8")
    manifest_path.write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print("10项来源已核对；只保留定位、hash与简短摘记，不保留第三方全文。")
    sys.exit(0)


def fetch(item):
    url = targets.get(item["id"], item["url"])
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 ResearchNotebook/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            content = response.read()
            item["http_status"] = response.status
            item["resolved_url"] = response.url
            mime = response.headers.get("Content-Type", "")
        text = content.decode("utf-8", errors="replace")
        if "html" in mime or text.lstrip().startswith("<"):
            text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", text, flags=re.S | re.I)
            text = re.sub(r"</(?:p|div|li|h[1-6]|pre|tr|section)>", "\n", text, flags=re.I)
            text = unescape(re.sub("<[^>]+>", " ", text))
            text = "\n".join(re.sub(r"\s+", " ", line).strip() for line in text.splitlines())
            text = re.sub(r"\n{3,}", "\n\n", text)
        output = BASE / "官方核查快照" / (item["id"] + ".txt")
        output.write_text(f"待核查摘记；下载hash：{hashlib.sha256(content).hexdigest()}\n", encoding="utf-8")
        item["snapshot"] = output.relative_to(BASE).as_posix()
        item["sha256_download"] = hashlib.sha256(content).hexdigest()
        item["status"] = "正文已抓取；相关段落与源码待本次人工核对"
        excerpts = []
        lines = text.splitlines()
        for pattern in patterns[item["id"]]:
            matches = [(i, line) for i, line in enumerate(lines) if pattern.lower() in line.lower()]
            for i, _ in matches[:2]:
                start, end = max(0, i - 1), min(len(lines), i + 3)
                excerpts.append("\n".join(f"{k+1}: {lines[k][:1000]}" for k in range(start, end)))
        item["matched_patterns"] = [p for p in patterns[item["id"]] if p.lower() in text.lower()]
        return item, f"\n{item['id']} {item['title']} ({len(text)} chars)\n" + "\n".join(excerpts)
    except Exception as exc:
        item["status"] = "抓取失败"
        item["error"] = str(exc)
        return item, f"\n{item['id']} ERROR {exc}"


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(fetch, items))
replacements = {i["id"]: i for i, _ in results}
manifest_path.write_text(json.dumps([replacements.get(i["id"], i) for i in all_items], ensure_ascii=False, indent=2), encoding="utf-8")
for _, summary in results:
    print(summary)
