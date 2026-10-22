"""从本地实验文档提取读数，复算统计，并生成科研记录图表。

用 Codex bundled Python 运行；matplotlib 额外目录通过环境变量 COWCV_PLOT_DEPS 指定。
不执行训练、不访问远程服务器、不修改来源文档。
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
from decimal import Decimal
from pathlib import Path

if os.environ.get("COWCV_PLOT_DEPS"):
    sys.path.insert(0, os.environ["COWCV_PLOT_DEPS"])

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parents[1]
RAW = ROOT / "牛只数据集"
NAVY, TEAL, BRONZE = "#17324d", "#19878b", "#b37b50"
INK, GRAY, PALE = "#20354a", "#647487", "#eef3f5"
FONT_PATH = Path("C:/Windows/Fonts/msyh.ttc")
BOLD_PATH = Path("C:/Windows/Fonts/msyhbd.ttc")
TABLES = []
LAYOUT_ERRORS = []


def dump(name, data):
    (ASSETS / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def rows(text):
    result = []
    for line in text.splitlines():
        if line.startswith("|"):
            cells = [re.sub(r"[*`]", "", c.strip()) for c in line.strip("|").split("|")]
            if not all(re.fullmatch(r"[-: ]+", c) for c in cells):
                result.append(cells)
    return result


def canonical(name):
    return "Google Open Image" if name.startswith("Google Open Image") else name


def dec(value):
    return Decimal(value.replace(",", ""))


ret_text = (RAW / "Retinanet测试.md").read_text(encoding="utf-8-sig")
yolo_text = (RAW / "yolo11SL.md").read_text(encoding="utf-8-sig")
ret_rows = rows(ret_text.split("## 3. 正式测试结果")[1].split("### 3.1")[0])[1:]
s_rows = rows(yolo_text.split("## 4. YOLO11s 正式评估结果")[1].split("## 5.")[0])[1:]
l_rows = rows(yolo_text.split("## 5. YOLO11l 正式评估结果")[1].split("## 6.")[0])[1:]
ret_data = {canonical(r[0]): r for r in ret_rows}
s_data = {canonical(r[0]): r for r in s_rows}
l_data = {canonical(r[0]): r for r in l_rows}
assert len(ret_data) == len(s_data) == len(l_data) == 14
assert set(ret_data) == set(s_data) == set(l_data)
NAMES = list(ret_data)
COMMON = [n for n in NAMES if s_data[n][1] == "val"]
TEST = [n for n in NAMES if s_data[n][1] == "test"]
assert len(COMMON) == 12 and TEST == ["Cows2021", "diarycow"]

data_rows = rows(ret_text.split("数据规模如下")[1].split("### 2.3")[0])[1:]
data_rows = [r for r in data_rows if r[0] != "合计"]
assert len(data_rows) == 14
data_data = {canonical(r[0]): r for r in data_rows}
totals = [sum(int(r[i].replace(",", "")) for r in data_rows) for i in range(1, 5)]
assert totals == [23851, 144723, 4971, 34864]

records = []
for n in NAMES:
    rr = ret_data[n]
    records.append(dict(dataset=n, model="RetinaNet", split="val", epoch_role="best val mAP50-95",
                        epoch=int(rr[1]), precision=None, recall=None,
                        map50=float(rr[3]), map5095=float(rr[2]), final_map5095=float(rr[4]),
                        source="牛只数据集/Retinanet测试.md §3"))
    for model, yy in (("YOLO11s", s_data[n]), ("YOLO11l", l_data[n])):
        records.append(dict(dataset=n, model=model, split=yy[1], epoch_role="results.csv peak; checkpoint epoch unverified",
                            epoch=int(yy[2]), precision=float(yy[3]), recall=float(yy[4]),
                            map50=float(yy[5]), map5095=float(yy[6]), final_map5095=None,
                            source=f"牛只数据集/yolo11SL.md §{'4' if model == 'YOLO11s' else '5'}"))
dump("逐数据集读数.json", records)
with (ASSETS / "逐数据集读数.csv").open("w", encoding="utf-8-sig", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(records)


def mean_for(model, metric, subset):
    values = []
    for n in subset:
        if model == "RetinaNet":
            values.append(dec(ret_data[n][3 if metric == "map50" else 2]))
        else:
            values.append(dec((s_data if model == "YOLO11s" else l_data)[n][5 if metric == "map50" else 6]))
    return sum(values) / len(values)


stats = {"basis": "对文档展示的四位/三位小数复算；不代表远程原始浮点精度",
         "counts": {"datasets": 14, "model_dataset_pairs": 42, "common_val_datasets": 12,
                    "yolo_test_datasets": 2, "train_images": totals[0], "train_boxes": totals[1],
                    "val_images": totals[2], "val_boxes": totals[3], "existing_test_images": 2551,
                    "retina_eval_images": 4971, "yolo_eval_images": 5939}}
stats["macros"] = {}
for subset_name, subset in (("14_original_protocols", NAMES), ("12_common_val", COMMON),
                            ("2_split_mismatches", TEST)):
    stats["macros"][subset_name] = {}
    for model in ("YOLO11s", "YOLO11l", "RetinaNet"):
        stats["macros"][subset_name][model] = {
            metric: str(mean_for(model, metric, subset)) for metric in ("map50", "map5095")}
diffs = {n: dec(l_data[n][6]) - dec(s_data[n][6]) for n in NAMES}
stats["yolo_l_minus_s"] = {
    "per_dataset": {n: str(v) for n, v in diffs.items()},
    "mean": str(sum(diffs.values()) / 14),
    "wins": sum(v > 0 for v in diffs.values()),
    "losses": sum(v < 0 for v in diffs.values()),
    "ties": sum(v == 0 for v in diffs.values())}
ret_final = sum(dec(ret_data[n][4]) for n in NAMES) / 14
ret_best = mean_for("RetinaNet", "map5095", NAMES)
ret_drop = {n: dec(ret_data[n][2]) - dec(ret_data[n][4]) for n in NAMES}
stats["retina_best_final"] = {
    "best_macro": str(ret_best), "final_macro": str(ret_final),
    "mean_drop": str(ret_best - ret_final),
    "CImage_drop": str(ret_drop["CImage"]),
    "CImage_share_of_total_drop": str(ret_drop["CImage"] / sum(ret_drop.values())),
    "mean_drop_excluding_CImage": str(sum(v for n, v in ret_drop.items() if n != "CImage") / 13),
    "best_epoch_le_10_count": sum(int(ret_data[n][1]) <= 10 for n in NAMES)}
stats["MooTrack360"] = {"train_boxes_per_image": str(Decimal(79072) / 1200),
                       "val_boxes_per_image": str(Decimal(19845) / 300)}
dump("统计复算.json", stats)

LOCAL_SOURCES = [
    ("L1", "牛只数据集/Retinanet测试.md", "§1–6"),
    ("L2", "牛只数据集/yolo11SL.md", "§1–9"),
    ("L3", "牛只数据集/_效率数据_远程日志提取_20260908.md", "训练时间线、batch补证；不采用推理排行榜"),
    ("L4", "牛只数据集/7月工作.md", "§13.6–13.7，跨划分重复审计"),
    ("L5", "科研记录/实验记录格式参考.md", "实验记录七项结构")]
source_hash_path = ASSETS / "来源文件hash.json"
if not source_hash_path.exists():
    dump("来源文件hash.json", [{"id": sid, "path": path, "locator": loc,
                              "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
                             for sid, path, loc in LOCAL_SOURCES])
for item in json.loads(source_hash_path.read_text(encoding="utf-8")):
    assert hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest() == item["sha256"]

EXTERNAL = [
    ("O1", "Ultralytics YOLO11", "https://docs.ultralytics.com/models/yolo11/", "模型系列与官方任务范围"),
    ("O2", "Ultralytics Model Validation", "https://docs.ultralytics.com/modes/val/", "model.val、split、conf、iou；当前文档不反证历史默认值"),
    ("O3", "Ultralytics Model Training", "https://docs.ultralytics.com/modes/train/", "训练参数与断点恢复的一般接口"),
    ("O4", "MMDetection 3.3.0 Customize Datasets", "https://mmdetection.readthedocs.io/en/v3.3.0/advanced_guides/customize_dataset.html", "类别映射与num_classes一致性"),
    ("O5", "MMDetection 3.3.0 Test existing models", "https://mmdetection.readthedocs.io/en/v3.3.0/user_guides/test.html", "tools/test.py与配置/权重参数"),
    ("O6", "MMDetection v3.3.0 RetinaNet config", "https://github.com/open-mmlab/mmdetection/blob/v3.3.0/configs/_base_/models/retinanet_r50_fpn.py", "FocalLoss、test_cfg；官方基础配置不等于历史有效配置"),
    ("O7", "Ultralytics v8.4.92 metrics.py", "https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/utils/metrics.py", "Metric.fitness L1009–1012；ap_per_class L885–886"),
    ("O8", "Ultralytics v8.4.92 trainer.py", "https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/engine/trainer.py", "save_model L712–714；validate L814–817"),
    ("O9", "COCO evaluation source", "https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py", "Params.setDetParams；IoU与maxDets"),
    ("O10", "Lin et al. Focal Loss for Dense Object Detection, ICCV 2017",
     "https://arxiv.org/abs/1708.02002", "§3 Focal Loss；§4 RetinaNet；原论文而非牛只实验")]
if not (ASSETS / "外部来源核查.json").exists():
    dump("外部来源核查.json", [{"id": sid, "title": title, "url": url, "locator": loc,
                              "checked": "2026-10-14", "status": "待正文与源码核查"}
                             for sid, title, url, loc in EXTERNAL])


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD_PATH if bold else FONT_PATH), size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for char in str(text):
        if char == "\n":
            lines.append(line)
            line = ""
        elif line and draw.textlength(line + char, font=fnt) > width:
            lines.append(line)
            line = char
        else:
            line += char
    lines.append(line)
    return lines


def table(number, title, headers, body, widths, note, size=36):
    """2400px、300dpi；每个单元格按实际字体测量并自适应行高。"""
    W, M = 2400, 100
    usable = W - 2 * M
    col = [int(usable * v / sum(widths)) for v in widths]
    col[-1] = usable - sum(col[:-1])
    probe = ImageDraw.Draw(Image.new("RGB", (W, 20)))
    fh, fb, fn = font(size, True), font(size), font(29)
    wrapped = [[wrap(probe, cell, fb, cw - 36) for cell, cw in zip(row, col)] for row in body]
    hh = max(len(wrap(probe, h, fh, cw - 36)) for h, cw in zip(headers, col)) * (size + 16) + 36
    heights = [max(len(c) for c in row) * (size + 16) + 30 for row in wrapped]
    note_lines = wrap(probe, note, fn, usable)
    H = 228 + hh + sum(heights) + len(note_lines) * 46 + 94
    im = Image.new("RGB", (W, H), "#fffefa")
    d = ImageDraw.Draw(im)
    d.rectangle((M, 50, M + 12, 151), fill=TEAL)
    d.text((M + 35, 53), f"表 {number}  {title}", font=font(49, True), fill=NAVY)
    d.text((M + 35, 126), "CATTLE DETECTION  /  EXPERIMENT RECORD", font=font(25), fill=GRAY)
    # 复用Study Image母版中的牛只轮廓图标，数值与中文均由本程序排字。
    mother = Image.open(ASSETS / "StudyImage-科研表格视觉母版.png").convert("RGB")
    mw, mh = mother.size
    icon = mother.crop((int(mw * .884), int(mh * .024), int(mw * .966), int(mh * .098)))
    icon.thumbnail((150, 138), Image.Resampling.LANCZOS)
    im.paste(icon, (W - M - icon.width, 42))
    y = 203
    d.line((M, y, W - M, y), fill=NAVY, width=4)
    x = M
    for h, cw in zip(headers, col):
        ls = wrap(d, h, fh, cw - 36)
        for k, line in enumerate(ls):
            d.text((x + 18, y + 18 + k * (size + 16)), line, font=fh, fill=NAVY)
        x += cw
    y += hh
    d.line((M, y, W - M, y), fill=NAVY, width=2)
    for row_index, (cells, height) in enumerate(zip(wrapped, heights)):
        if row_index % 2 == 0:
            d.rectangle((M, y + 2, W - M, y + height), fill=PALE)
        x = M
        for idx, (ls, cw) in enumerate(zip(cells, col)):
            text_y = y + (height - len(ls) * (size + 16)) / 2
            for k, line in enumerate(ls):
                if d.textlength(line, font=fb) > cw - 35:
                    LAYOUT_ERRORS.append(f"table{number}:row{row_index}:col{idx}")
                d.text((x + 18, text_y + k * (size + 16)), line, font=fb, fill=INK)
            x += cw
        y += height
        d.line((M, y, W - M, y), fill="#d6e0e5", width=1)
    d.line((M, y, W - M, y), fill=NAVY, width=3)
    for k, line in enumerate(note_lines):
        d.text((M, y + 29 + k * 46), line, font=fn, fill=GRAY)
    filename = f"表{number}-{title}.png"
    im.save(ASSETS / filename, dpi=(300, 300))
    TABLES.append({"number": number, "title": title, "file": filename,
                   "headers": headers, "rows": body, "note": note})


table(1, "模型环境与训练协议", ["项目", "YOLO11s", "YOLO11l", "RetinaNet R50-FPN"], [
    ["框架", "Ultralytics 8.4.92", "Ultralytics 8.4.92", "MMDetection 3.3.0"],
    ["Python / PyTorch", "3.10.18 / 2.5.1+cu124", "3.10.18 / 2.5.1+cu124", "3.10 / 2.1.0+cu121"],
    ["GPU / 训练轮数", "A100-PCIE-40GB / 100", "A100-PCIE-40GB / 100", "A100-PCIE-40GB / 100"],
    ["输入设置", "imgsz=640；原文写640×640", "imgsz=640；原文写640×640", "1333×800；保持宽高比"],
    ["训练物理batch", "L2配置表16；命令/L3为32", "L2配置表16；命令/L3为32", "2；累积8次，名义有效16"],
    ["训练精度 / workers", "AMP开启 / 8", "AMP开启 / 8", "FP32，AMP关闭 / 4"],
    ["seed / 确定性", "42 / deterministic=True", "42 / deterministic=True", "0 / 原文未说明"],
    ["初始化", "COCO预训练 yolo11s.pt", "COCO预训练 yolo11l.pt", "COCO预训练R50-FPN"],
    ["优化与增强", "实际args.yaml待核对", "实际args.yaml待核对", "SGD，lr=0.01；水平翻转0.5"],
    ["评估视图", "12 val + 2 test", "12 val + 2 test", "14 val"],
    ["权重选择", "使用best.pt；具体epoch待核对", "使用best.pt；具体epoch待核对", "验证bbox_mAP最大epoch"],
], [1.05, 1.75, 1.75, 1.85], "来源：L1 §1/2.3；L2 §1/2.3–3；L3时间线。100 epochs不代表优化步数、算力或选模规则一致。", 33)

body = []
for n in NAMES:
    dr = data_data[n]
    body.append([n, *dr[1:5], "2,131" if n == "Cows2021" else "420" if n == "diarycow" else "—",
                 "val / test" if n in TEST else "val / val"])
body.append(["合计", "23,851", "144,723", "4,971", "34,864", "2,551", "R:4,971 / Y:5,939"])
table(2, "数据规模与评估视图", ["数据集", "train图像", "train框", "val图像", "val框", "test图像", "实际评估 R / Y"],
      body, [2.3, 1, 1.1, 1, 1, 1, 1.7],
      "来源：L1 §2.2；L2 §2.2。R=RetinaNet，Y=两个YOLO；test框数量未给出。Google名称统一为同一条目，成员一致性仍需hash清单核对。", 33)

table(3, "三模型逐域mAP50-95", ["数据集", "split R / Y", "YOLO11s", "YOLO11l", "RetinaNet", "L−S（pp）"],
      [[n, "val / test" if n in TEST else "val / val", s_data[n][6], l_data[n][6],
        f"{dec(ret_data[n][2]):.4f}", f"{diffs[n] * 100:+.2f}"] for n in NAMES],
      [2.4, 1.4, 1, 1, 1, 1.2],
      "来源：L1 §3；L2 §4–5。pp=百分点；R为验证峰值，Y为best.pt复评。即使同为val，输入、框架与seed仍不同；不标跨架构冠军。", 35)

table(4, "YOLO辅助读数与RetinaNet AP50", ["数据集", "S: P / R", "L: P / R", "S: AP50", "L: AP50", "R: AP50"],
      [[n, f"{s_data[n][3]} / {s_data[n][4]}", f"{l_data[n][3]} / {l_data[n][4]}",
        s_data[n][5], l_data[n][5], f"{dec(ret_data[n][3]):.4f}"] for n in NAMES],
      [2.45, 2, 2, 1, 1, 1],
      "来源：L1 §3；L2 §4–5。YOLO P/R保留原文默认工作点，不能改称固定conf=0.25；RetinaNet逐域P/R未记录，不补造。", 33)

table(5, "选模轮次与末轮回落", ["数据集", "S峰值epoch", "L峰值epoch", "R最佳epoch", "R第100轮AP", "R峰值−末轮"],
      [[n, s_data[n][2], l_data[n][2], ret_data[n][1], f"{dec(ret_data[n][4]):.4f}",
        f"{ret_drop[n]:.4f}"] for n in NAMES],
      [2.5, 1.15, 1.15, 1.15, 1.3, 1.3],
      "来源：L1 §3；L2 §4–5。AP指mAP50–95。S/L峰值来自results.csv，不能当作已核实的best.pt epoch；未给出S/L末轮AP。", 34)

macro_body = []
for label, group in (("14域原协议：12同val+2异split", "14_original_protocols"),
                     ("12域共同val（仍非统一实现）", "12_common_val"),
                     ("2域：R val / Y test", "2_split_mismatches")):
    for metric, lab in (("map5095", "mAP50–95"), ("map50", "mAP50")):
        macro_body.append([label, lab, *[f"{Decimal(stats['macros'][group][m][metric]):.4f}"
                                         for m in ("YOLO11s", "YOLO11l", "RetinaNet")]])
table(6, "分协议等权宏平均", ["汇总范围", "指标", "YOLO11s", "YOLO11l", "RetinaNet"], macro_body,
      [2.7, 1.2, 1, 1, 1],
      "根据正文展示读数等权复算；每域一票，不按框数加权。14域与2域含split差异；12域仅减少该差异，仍不能支持纯架构或显著性结论。", 35)

table(7, "异常与证据冲突复盘", ["问题", "已见证据", "本记录处理", "待核查产物"], [
    ["训练batch不一致", "L2表=16；命令=32；L3=32", "并列保留；不把训练与评估batch混同", "每run args.yaml与训练进度日志"],
    ["峰值与best身份", "L2称综合fitness；O7仅用AP50–95", "保留原始读数；不采纳未经证实的原因", "安装源码hash、checkpoint epoch/EMA"],
    ["CImage后期回落", "R:0.694→0.087；S/L峰值epoch=1", "回落是事实；过拟合/不稳定是候选解释", "逐轮loss、预测、学习率及数据分布"],
    ["train/评估重复", "diarycow 18/4/5；NWAFU 5；XGain 3", "标记污染；重叠集合不可直接相加", "重复成员表与清理后冻结清单"],
    ["评估split不同", "两域R=val，S/L=test", "表中逐行标明；另算12域共同val", "三模型同test视图与统一评估JSON"],
    ["YOLO评估入口异常", "L2记录--all空列表/choices报错", "已修复属历史记录；本次未重跑", "evaluate脚本提交与成功状态文件"],
], [1.2, 2.05, 2.35, 1.9], "来源：L1 §2–4；L2 §2.3/3.1/4/8；L3；L4 §13.6；O7/O8。官方默认配置与原文记录均不能替代远程有效配置。", 32)

table(8, "后续复核与验收", ["顺序", "具体任务", "应保存产物", "验收条件"], [
    ["1 配置身份", "核对batch、优化器、积累、seed、权重与源码", "args/effective_config、环境清单、权重hash", "42个run均有明确身份；冲突可解释"],
    ["2 数据隔离", "核对精确/近重复、视频/牛ID来源组与框语义", "成员级清单、split_manifest、label审计", "已知训练到评估污染清理且可追溯"],
    ["3 同集重评", "冻结共同test，统一类别、评估器和预测后处理", "每图预测JSON、AP/P/R设置、评估配置", "同目标域三模型使用相同样本与GT"],
    ["4 稳定性", "增加至少3个预先声明seed；按来源簇估计不确定性", "逐seed表、来源簇划分、区间估计", "报告方差/区间；不把14域当14次独立重复"],
    ["5 部署实测", "同硬件、输入、精度和负载下测任务权重", "warmup/重复次数、P50/P95、显存与硬件状态", "三模型完整记录；与预训练benchmark分表"],
], [1.05, 2.7, 2.4, 2.4], "全部为后续计划，尚未执行。早停/阈值仅用val确定；新划分与新协议的结果单独标版本，不能覆盖历史读数。", 32)

dump("表格结构数据.json", TABLES)
md = ["# 三种模型测试：表格可编辑底稿", "", "> 与正文PNG同源生成；来源与限制随表保留。", ""]
for tab in TABLES:
    md += [f"## 表 {tab['number']}　{tab['title']}", "",
           "| " + " | ".join(tab["headers"]) + " |",
           "| " + " | ".join(["---"] * len(tab["headers"])) + " |"]
    md += ["| " + " | ".join(str(c).replace("\n", "<br>") for c in row) + " |" for row in tab["rows"]]
    md += ["", tab["note"], ""]
(ASSETS / "表格可编辑底稿.md").write_text("\n".join(md), encoding="utf-8")

# 将研究概览保留为概念图，并在图内明确其证据身份。
orig = Image.open(ASSETS / "StudyImage-三模型研究概览原图.png").convert("RGB")
W = 2400
orig = orig.resize((W, W), Image.Resampling.LANCZOS)
overview = Image.new("RGB", (W, W + 125), "#fffefa")
overview.paste(orig)
od = ImageDraw.Draw(overview)
od.text((90, W + 33), "模型与评估概念示意 · 方框非真实预测 · 模块非精确网络结构", font=font(36), fill=GRAY)
overview.save(ASSETS / "图1-三模型研究概览.png", dpi=(300, 300))

# 精确的历史流程图，不把test画成RetinaNet已有历史输出。
flow = Image.new("RGB", (2400, 1200), "#fffefa")
fd = ImageDraw.Draw(flow)
fd.text((95, 52), "历史实验流程与评估分流", font=font(61, True), fill=NAVY)
fd.text((95, 142), "先冻结数据视图，再按各模型既有协议训练、选模与复评", font=font(36), fill=GRAY)


def box(x, y, w, h, heading, lines, color=TEAL):
    fd.rounded_rectangle((x, y, x + w, y + h), radius=22, outline=color, width=4, fill="#f4f7f7")
    fd.text((x + 25, y + 24), heading, font=font(40, True), fill=color)
    for i, line in enumerate(lines):
        fd.text((x + 25, y + 88 + i * 58), line, font=font(33), fill=INK)


def arrow(x1, y1, x2, y2):
    fd.line((x1, y1, x2, y2), fill=GRAY, width=6)
    fd.polygon([(x2, y2), (x2 - 18, y2 - 12), (x2 - 18, y2 + 12)], fill=GRAY)


box(100, 275, 550, 505, "14个冻结训练视图", ["单类别 cow", "图片/标签配对预检", "保留原始资料", "COCO / YOLO 两种表达", "成员hash仍需逐项核对"], NAVY)
box(790, 250, 670, 265, "RetinaNet R50-FPN", ["100 epochs；每轮val", "取最大 bbox_mAP 的权重"], BRONZE)
box(790, 640, 670, 265, "YOLO11s / YOLO11l", ["100 epochs；按val选best.pt", "重新加载权重执行评估"], TEAL)
box(1600, 250, 700, 265, "RetinaNet历史输出", ["14个val", "保存最佳与第100轮读数"], BRONZE)
box(1600, 640, 700, 265, "YOLO历史复评输出", ["12个val + 2个test", "Cows2021 / diarycow 使用test"], TEAL)
arrow(650, 380, 790, 380)
arrow(650, 765, 790, 765)
arrow(1460, 380, 1600, 380)
arrow(1460, 765, 1600, 765)
fd.line((100, 1000, 2300, 1000), fill="#cedce0", width=2)
fd.text((110, 1038), "分析：逐域读数 → 按split分组 → 等权复算 → 异常复盘 → 共同test后续计划", font=font(37, True), fill=NAVY)
fd.text((110, 1110), "历史流程依据L1/L2；这次仅整理与复算。未重新训练或评估。", font=font(30), fill=GRAY)
flow.save(ASSETS / "图2-历史流程与评估分流.png", dpi=(300, 300))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

FP = FontProperties(fname=str(FONT_PATH))
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Microsoft YaHei"],
                     "axes.unicode_minus": False, "figure.facecolor": "#fffefa",
                     "axes.facecolor": "#fffefa", "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": GRAY, "ytick.color": INK, "font.size": 12})


def clean(ax):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#cad5dd")
    ax.grid(axis="x", color="#dbe3e8", lw=.7)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)


def finish(fig, filename):
    fig.savefig(ASSETS / filename, dpi=300, facecolor="#fffefa")
    plt.close(fig)


fig, ax = plt.subplots(figsize=(8, 6.3))
fig.subplots_adjust(left=.29, right=.9, top=.84, bottom=.16)
ys = np.arange(14)
values = [float(diffs[n] * 100) for n in NAMES]
ax.barh(ys, values, color=[TEAL if v > 0 else BRONZE for v in values], height=.59)
ax.axvline(0, color=NAVY, lw=1)
ax.set_yticks(ys, [n + (" †" if n in TEST else "") for n in NAMES], fontsize=10)
ax.invert_yaxis()
ax.set_xlim(-1.65, 3.05)
for y, v in zip(ys, values):
    ax.text(v + (.07 if v >= 0 else -.07), y, f"{v:+.2f}", va="center",
            ha="left" if v >= 0 else "right", fontsize=10, color=INK)
ax.set_xlabel("YOLO11l − YOLO11s：mAP50–95 差值（百分点）", fontproperties=FP, fontsize=11)
clean(ax)
fig.text(.08, .94, "模型容量增加，收益随数据集变化", fontproperties=FP, fontsize=17, color=NAVY)
fig.text(.08, .89, f"同一YOLO系列历史读数：L提高9/14；宏平均增加 {float(stats['yolo_l_minus_s']['mean'])*100:.2f} pp",
         fontproperties=FP, fontsize=10, color=GRAY)
fig.text(.08, .055, "† 两个YOLO均使用test；其余为val。单seed、既有划分，不作显著性判断。", fontproperties=FP, fontsize=9, color=GRAY)
finish(fig, "图3-YOLO逐域容量收益.png")

fig, ax = plt.subplots(figsize=(8, 6.3))
fig.subplots_adjust(left=.29, right=.96, top=.84, bottom=.16)
for i, n in enumerate(NAMES):
    best, final = float(ret_data[n][2]), float(ret_data[n][4])
    ax.plot([final, best], [i, i], color=BRONZE if n == "CImage" else "#c5d4dc",
            lw=4 if n == "CImage" else 2)
ax.scatter([float(ret_data[n][2]) for n in NAMES], ys, color=TEAL, s=34, label="验证峰值")
ax.scatter([float(ret_data[n][4]) for n in NAMES], ys, color=BRONZE, s=28, marker="s", label="第100轮")
ax.set_yticks(ys, NAMES, fontsize=10)
ax.invert_yaxis()
ax.set_xlim(0, 1.02)
ax.set_xlabel("RetinaNet mAP50–95（各域val）", fontproperties=FP, fontsize=11)
ax.legend(loc="lower left", bbox_to_anchor=(0, 1.01), ncol=2, frameon=False, prop=FP, fontsize=10)
ax.text(.33, 4-.28, "CImage：0.694 → 0.087", fontproperties=FP, fontsize=10, color=BRONZE)
clean(ax)
fig.text(.08, .94, "最佳权重与末轮权重，需要分开记录", fontproperties=FP, fontsize=17, color=NAVY)
fig.text(.08, .055, "仅连接两个已记录端点，不表示逐轮训练曲线；CImage下降60.7个百分点。", fontproperties=FP, fontsize=9, color=GRAY)
finish(fig, "图4-RetinaNet峰值与末轮.png")

fig, ax = plt.subplots(figsize=(8, 3.9))
fig.subplots_adjust(left=.22, right=.93, top=.71, bottom=.25)
for i, (model, color) in enumerate((("YOLO11s", NAVY), ("YOLO11l", TEAL), ("RetinaNet", BRONZE))):
    ap = float(stats["macros"]["12_common_val"][model]["map5095"])
    ap50 = float(stats["macros"]["12_common_val"][model]["map50"])
    ax.plot([ap, ap50], [i, i], color=color, lw=2.5)
    ax.scatter([ap, ap50], [i, i], s=[65, 65], marker="o", color=color)
    ax.annotate(f"{ap:.4f}", (ap, i), xytext=(0, -13), textcoords="offset points",
                ha="center", va="top", fontsize=11, color=color)
    ax.annotate(f"{ap50:.4f}", (ap50, i), xytext=(0, -13), textcoords="offset points",
                ha="center", va="top", fontsize=11, color=color)
ax.set_yticks([0, 1, 2], ["YOLO11s", "YOLO11l", "RetinaNet"])
ax.invert_yaxis()
ax.set_xlim(.64, .96)
ax.set_ylim(2.65, -.65)
ax.set_xlabel("12个共同val的等权宏平均（左：AP50–95；右：AP50）", fontproperties=FP, fontsize=10)
clean(ax)
fig.text(.08, .93, "较宽松的AP50，不能替代严格定位指标", fontproperties=FP, fontsize=16, color=NAVY)
fig.text(.08, .83, "移除两个split不一致数据集后的描述性读数", fontproperties=FP, fontsize=11, color=GRAY)
fig.text(.08, .075, "同为val仍有输入、框架、seed和选模差异；此图不建立统一架构排名。", fontproperties=FP, fontsize=9, color=GRAY)
finish(fig, "图5-共同val定位指标.png")

# 便于逐幅审核的图表总览。
files = [ASSETS / "图1-三模型研究概览.png", ASSETS / "图2-历史流程与评估分流.png",
         *[ASSETS / t["file"] for t in TABLES],
         ASSETS / "图3-YOLO逐域容量收益.png", ASSETS / "图4-RetinaNet峰值与末轮.png",
         ASSETS / "图5-共同val定位指标.png"]
thumb_w, thumb_h = 710, 630
contact = Image.new("RGB", (thumb_w * 3, thumb_h * 5), "#e7edf0")
cd = ImageDraw.Draw(contact)
for i, path in enumerate(files):
    thumb = Image.open(path).convert("RGB")
    thumb.thumbnail((thumb_w - 36, thumb_h - 80), Image.Resampling.LANCZOS)
    xx, yy = (i % 3) * thumb_w, (i // 3) * thumb_h
    cd.text((xx + 20, yy + 15), path.stem[:28], font=font(25, True), fill=NAVY)
    contact.paste(thumb, (xx + (thumb_w - thumb.width) // 2, yy + 64))
contact.save(ASSETS / "图表校阅总览.jpg", quality=94)
dump("排版测量.json", {"cell_overflow_errors": LAYOUT_ERRORS,
                       "figure_table_count": len(files), "tables": len(TABLES), "figures": 5,
                       "table_width_px": 2400, "table_dpi": 300})
assert not LAYOUT_ERRORS
print(json.dumps(stats, ensure_ascii=False, indent=2))
print("完成：42个模型/数据集读数；8表5图；来源hash未变；单元格无溢出。")
