"""从本地文档复算历史域内结果，并排版科研记录图表；不写入原始资料。"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import statistics as st
from itertools import combinations
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
DRAFT = ROOT / "牛只数据集/文章初稿.md"
AUDIT = ROOT / "牛只数据集/域内模型与架构比较.md"
NAVY, TEAL, BLUE, GOLD = "#183A56", "#168B84", "#4B80B2", "#C18032"
MUTED, RULE, LIGHT = "#536779", "#CCD8E0", "#F0F5F8"
COLORS = [TEAL, BLUE, GOLD, "#8889A8"]
MODELS = ["YOLO11m", "RT-DETR-L", "Faster R-CNN", "RetinaNet"]
W, M = 2400, 90


def font(size, bold=False):
    p = "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"
    return ImageFont.truetype(p, size)


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def first_table(text, marker):
    body = text.split(marker, 1)[1]
    lines = body.splitlines()
    found, rows = False, []
    for line in lines:
        if line.startswith("|"):
            found = True
            rows.append([x.strip() for x in line.strip().strip("|").split("|")])
        elif found:
            break
    assert len(rows) > 2, marker
    return rows[0], rows[2:]


def numeric_table(text, marker):
    _, rows = first_table(text, marker)
    return {r[0]: [float(x) for x in r[1:]] for r in rows}


def wrap(text, f, width):
    out = []
    for paragraph in str(text).split("\n"):
        current = ""
        for token in re.findall(r"[A-Za-z0-9_]+(?:[-.][A-Za-z0-9_]+)*|\s+|.", paragraph):
            if current and f.getlength(current + token) > width:
                if token in "，。；：、！？）】》":
                    last = re.search(r"([A-Za-z0-9_]+(?:[-.][A-Za-z0-9_]+)*|.)$", current.rstrip())
                    cut = last.start() if last else len(current)
                    if cut > 0:
                        out.append(current[:cut].rstrip())
                        current = current[cut:].strip() + token
                    else:
                        current += token
                else:
                    out.append(current.rstrip())
                    current = token.lstrip()
            else:
                current += token
        out.append(current)
    return out


def save_png(img, name):
    img.save(BASE / f"{name}.png", dpi=(300, 300))


def surface(height, title, subtitle):
    bg = Image.open(BASE / "科研表格版式母图.png").convert("RGB")
    # Study Image 生成母版的细边保留；正文区以白底精确排字。
    bg = bg.resize((W, height))
    d = ImageDraw.Draw(bg)
    d.rectangle((28, 22, W - 28, height - 22), fill="white")
    d.rectangle((M, 54, M + 10, 117), fill=TEAL)
    d.text((M + 30, 45), title, fill=NAVY, font=font(56, True))
    d.text((M + 30, 124), subtitle, fill=MUTED, font=font(33))
    return bg, d


draft = DRAFT.read_text(encoding="utf-8-sig")
audit = AUDIT.read_text(encoding="utf-8-sig")
map95 = numeric_table(draft, "四个检测器当前记录的 `mAP@0.5:0.95`")
map50 = numeric_table(draft, "对应的 `mAP@0.5` 记录如下")
epochs = numeric_table(audit, "### 3.5 最佳轮次")
_, fixed_rows = first_table(draft, "三项指标合并列示")
fixed = {r[0]: [[float(v.strip()) for v in x.split("/")] for x in r[1:]]
         for r in fixed_rows}
_, best_rows = first_table(draft, "### 附表 A1")
best = {r[0]: [[float(v.strip()) for v in x.split("/")] for x in r[1:]]
        for r in best_rows}
_, split_rows = first_table(draft, "当前14个数据集共包含31,373张图像")
datasets = list(map95)
assert all(set(x) == set(datasets) for x in (map50, epochs, fixed, best))
assert len(datasets) == 14 and all(len(x) == 4 for x in map95.values())


def rank(values):
    return [sorted(values).index(v) + 1 for v in values]  # 当前 14 项均无并列


means95 = [st.mean(v[i] for v in map95.values()) for i in range(4)]
means50 = [st.mean(v[i] for v in map50.values()) for i in range(4)]
fixed_mean = [[st.mean(v[i][j] for v in fixed.values()) for j in range(3)]
              for i in range(4)]
best_mean = [[st.mean(v[i][j] for v in best.values()) for j in range(1, 4)]
             for i in range(4)]
diff = {k: v[1] - v[0] for k, v in map95.items()}
domain_mean = {k: st.mean(v) for k, v in map95.items()}
correlations = {}
for i, j in combinations(range(4), 2):
    x = rank([v[i] for v in map95.values()])
    y = rank([v[j] for v in map95.values()])
    correlations[f"{MODELS[i]} / {MODELS[j]}"] = 1 - 6 * sum(
        (a - b) ** 2 for a, b in zip(x, y)) / (14 * (14 ** 2 - 1))
stats = {
    "口径": "本地已公开表格复算；保留源表精度，不代表重新读取远程全精度结果",
    "模型": MODELS, "K": 14, "训练组合数": 56,
    "mAP50-95宏平均": means95, "mAP50宏平均": means50,
    "固定阈值PRF宏平均_从三位小数逐域表复算": fixed_mean,
    "最佳工作点PRF宏平均_从三位小数逐域表复算": best_mean,
    "RT减YOLO差值": diff, "RT领先域数": sum(v > 0 for v in diff.values()),
    "YOLO领先域数": sum(v < 0 for v in diff.values()),
    "差值宏平均": st.mean(diff.values()),
    "绝对差均值": st.mean(abs(v) for v in diff.values()),
    "绝对差不超过0.02的域数": sum(abs(v) <= .02 for v in diff.values()),
    "Spearman": correlations,
    "数据集四模型均值": domain_mean,
    "数据集均值跨度": max(domain_mean.values()) - min(domain_mean.values()),
    "模型宏平均跨度": max(means95) - min(means95),
    "输入设置矩形面积比": 1333 * 800 / (640 * 640),
    "AP50与AP50-95差值": {k: st.mean(map50[k]) - st.mean(map95[k]) for k in datasets},
    "mAP50-95描述统计": {
        MODELS[i]: {
            "中位数": st.median([v[i] for v in map95.values()]),
            "Q1_Q3_inclusive": [
                st.quantiles([v[i] for v in map95.values()], n=4, method="inclusive")[0],
                st.quantiles([v[i] for v in map95.values()], n=4, method="inclusive")[2]],
            "最小值": min(v[i] for v in map95.values())}
        for i in range(4)},
}
assert (stats["RT领先域数"], stats["YOLO领先域数"]) == (9, 5)
assert stats["绝对差不超过0.02的域数"] == 12
assert abs(means95[0] - .7389714285714286) < 1e-12
assert abs(means95[1] - .7436785714285714) < 1e-12
dump(BASE / "数值复算.json", stats)
data = {"datasets": datasets, "models": MODELS, "map95": map95, "map50": map50,
        "fixed_prf": fixed, "best_thr_prf": best, "best_map_epoch": epochs}
dump(BASE / "图表数据.json", data)
with (BASE / "逐模型逐数据集指标.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["dataset", "model", "split", "map50_95", "map50", "P@0.25",
                     "R@0.25", "F1@0.25", "conf_best", "P_best", "R_best",
                     "F1_best", "map_peak_epoch"])
    for k in datasets:
        for i in range(4):
            writer.writerow([k, MODELS[i], "val", map95[k][i], map50[k][i],
                             *fixed[k][i], *best[k][i], int(epochs[k][i])])


def short_name(k):
    return {"NWAFU Cattle Dataset": "NWAFU Cattle",
            "COCO cow subset": "COCO cow",
            "Google Open Images cow subset": "Google Open Images cow"}.get(k, k)


def table(name, title, subtitle, headers, rows, widths, note, size=39):
    assert sum(widths) == W - 2 * M and all(len(r) == len(headers) for r in rows)
    f, hf, nf = font(size), font(size, True), font(31)
    line = size + 17
    hlines = [wrap(v, hf, widths[i] - 42) for i, v in enumerate(headers)]
    head_h = max(map(len, hlines)) * line + 38
    contents = [[wrap(v, f, widths[i] - 42) for i, v in enumerate(r)] for r in rows]
    heights = [max(map(len, r)) * line + 28 for r in contents]
    notes = wrap(note, nf, W - 2 * M)
    height = 213 + head_h + sum(heights) + len(notes) * 44 + 104
    img, d = surface(height, title, subtitle)
    y = 209
    d.rectangle((M, y, W - M, y + head_h), fill=LIGHT)
    d.line((M, y, W - M, y), fill=NAVY, width=4)
    x = M
    for i, lines in enumerate(hlines):
        for n, text in enumerate(lines):
            d.text((x + 20, y + 18 + n * line), text, fill=NAVY, font=hf)
        x += widths[i]
    y += head_h
    d.line((M, y, W - M, y), fill=NAVY, width=2)
    for r_index, (r, rh) in enumerate(zip(contents, heights)):
        if r_index % 2:
            d.rectangle((M, y, W - M, y + rh), fill="#F8FAFB")
        x = M
        for i, lines in enumerate(r):
            for n, text in enumerate(lines):
                d.text((x + 20, y + 14 + n * line), text, fill=NAVY, font=f)
            x += widths[i]
        y += rh
        d.line((M, y, W - M, y), fill=RULE, width=1)
    d.line((M, y, W - M, y), fill=NAVY, width=4)
    for n, text in enumerate(notes):
        d.text((M, y + 30 + n * 44), text, fill=MUTED, font=nf)
    save_png(img, name)
    return {"name": name, "title": title, "subtitle": subtitle, "headers": headers,
            "rows": rows, "note": note, "width": W, "height": height, "dpi": 300}


tables = []


def add(*args, **kwargs):
    tables.append(table(*args, **kwargs))


add("表1-数据覆盖", "表 1　历史工作集与本节评估覆盖",
    "2026-07 数据视图｜四模型主表均评估 val；test 数量只登记历史划分",
    ["数据集", "train", "val", "名义 test", "图像合计"],
    [[short_name(r[0].strip("*").replace("Cattle Body Parts（训练名 CBPD_ODD）", "CBPD_ODD")
                 .replace("Holstein Cattle Recognition Images（训练名 HCRD）", "HCRD")
                 .replace("Cow-images（训练名 CImage）", "CImage")),
      *r[2].strip("*").split("/"), r[1].strip("*").replace(",", "")]
     for r in split_rows],
    [760, 340, 340, 360, 420],
    "来源：L2 §3.2。Dairy Cow / Cows2021 的历史 test 登记不构成本节独立测试；数据版本与 10 月重测不同。",
    size=36)
add("表2-训练配置", "表 2　四种检测器的历史训练配置",
    "100 epochs 为共同名义轮数｜有效 batch 指稳态近似，不替代更新次数日志",
    ["项目", "YOLO11m", "RT-DETR-L", "Faster R-CNN", "RetinaNet"],
    [
        ["框架", "Ultralytics\n8.4.92", "Ultralytics\n8.4.92", "MMDetection\n3.3.0", "MMDetection\n3.3.0"],
        ["初始化", "COCO 预训练\nyolo11m.pt", "COCO 预训练\nrtdetr-l.pt", "COCO 官方\nR50-FPN 1x", "COCO 官方\nR50-FPN 1x"],
        ["名义轮数", "100", "100", "100", "100"],
        ["micro-batch", "16（3 域）\n32（11 域）", "12（14 域）", "16（6 域）\n2（8 域）", "2（14 域）"],
        ["稳态累积次数", "4 / 2", "5", "1 / 8", "8"],
        ["稳态有效 batch", "64", "60", "16", "16"],
        ["AMP", "True", "False", "False", "False"],
        ["实际优化器", "AdamW\nlr=0.002", "MuSGD\nlr=0.01", "SGD\nlr=0.02", "SGD\nlr=0.01"],
        ["输入尺寸设置", "640 × 640", "640 × 640\n变换待核查", "Resize\n(1333, 800)", "Resize\n(1333, 800)"],
        ["随机种子", "0", "0", "0", "0"],
    ], [340, 470, 470, 470, 470],
    "来源：L1 §1；L2 §4.1。nbs=64 不保证 RT-DETR 有效 batch 恰为 64；warmup、末批与执行路径需另外记录。",
    size=35)
add("表3-软件环境", "表 3　训练时环境与适用范围",
    "共同硬件：单卡 NVIDIA A100-PCIE-40GB｜历史环境与当前环境分开登记",
    ["项目", "YOLO11m / RT-DETR-L", "Faster R-CNN / RetinaNet"],
    [
        ["Conda 环境", "ultralytics（历史训练时）", "mmdetection"],
        ["Python", "3.10.18", "3.10.10"],
        ["PyTorch", "2.6.0+cu118", "2.1.0+cu121"],
        ["PyTorch CUDA 构建", "11.8", "12.1"],
        ["检测框架", "Ultralytics 8.4.92", "MMDetection 3.3.0"],
        ["其他依赖", "其余依赖以历史快照复核", "TorchVision 0.16.0+cu121\nMMCV 2.1.0 / MMEngine 0.10.7"],
        ["训练时段", "YOLO：07-11 至 07-16\nRT-DETR：07-17 至 07-18", "Faster：07-25 至 07-28\nRetinaNet：08-04 至 08-06"],
    ], [460, 880, 880],
    "来源：L1 §2；L2 §4.1。07-24 恢复后的 torch 2.5.1+cu124 属另一环境快照，不能倒填历史训练版本。",
    size=38)
add("表4-最佳轮次", "表 4　验证 mAP@0.5:0.95 的最高轮次",
    "历史 56 组训练的峰值轮次｜不将峰值轮次自动解释为 best.pt 文件身份",
    ["数据集", *MODELS],
    [[short_name(k), *[str(int(v)) for v in epochs[k]]] for k in datasets],
    [740, 370, 370, 370, 370],
    "来源：L1 §3.5。Ultralytics 为 results.csv 峰值轮；MMDetection 为所记录的 best_coco_bbox_mAP checkpoint 轮。",
    size=36)
add("表5-mAP主结果", "表 5　14 个数据集的阶段性域内验证结果",
    "mAP@0.5:0.95｜每格来自该模型在该数据集上独立训练的结果",
    ["数据集", *MODELS],
    [[short_name(k), f"{map95[k][0]:.4f}", f"{map95[k][1]:.4f}",
      f"{map95[k][2]:.3f}", f"{map95[k][3]:.3f}"] for k in datasets],
    [740, 370, 370, 370, 370],
    "来源：L2 §4.3.1。保留源表的小数精度；全部为 val，不标显著性星号，不据此作普遍架构排名。",
    size=36)
add("表6-固定阈值F1", "表 6　统一工作点下的 F1",
    "conf=0.25；匹配 IoU≥0.5｜逐域 P / R / F1 完整底稿另存",
    ["数据集", *MODELS],
    [[short_name(k), *[f"{fixed[k][i][2]:.3f}" for i in range(4)]] for k in datasets],
    [740, 370, 370, 370, 370],
    "来源：L2 §4.3.1。固定阈值结果和扫描 mAP 的工作点不同；历史预测集合与后处理差异仍需核查。",
    size=36)
add("表7-宏平均", "表 7　14 个数据集等权宏平均",
    "K=14｜AP 由公开表复算；P / R / F1 沿用原文三位小数汇总",
    ["检测器", "mAP50-95", "mAP50", "P@0.25", "R@0.25", "F1@0.25"],
    [
        ["YOLO11m", f"{means95[0]:.4f}", f"{means50[0]:.4f}", "0.870", "0.917", "0.893"],
        ["RT-DETR-L", f"{means95[1]:.4f}", f"{means50[1]:.4f}", "0.719", "0.946", "0.807"],
        ["Faster R-CNN", f"{means95[2]:.4f}", f"{means50[2]:.4f}", "0.825", "0.930", "0.869"],
        ["RetinaNet", f"{means95[3]:.4f}", f"{means50[3]:.4f}", "0.778", "0.922", "0.839"],
    ], [620, 320, 320, 320, 320, 320],
    "来源：L2 §4.3.1–4.3.2。宏平均 F1 是 14 个 F1 的平均，不由宏平均 P 和 R 再计算；四位 AP 为派生统计。",
    size=35)
add("表8-定位差距", "表 8　宽松与严格定位指标的差距",
    "每行先对四模型等权平均｜差值仅用于指标层面诊断",
    ["数据集", "平均 AP50", "平均 AP50-95", "差值"],
    [[short_name(k), f"{st.mean(map50[k]):.4f}", f"{st.mean(map95[k]):.4f}",
      f"{st.mean(map50[k])-st.mean(map95[k]):.4f}"]
     for k in ["8-calves", "MooTrack360", "COLO", "COCO cow subset",
               "Google Open Images cow subset"]],
    [840, 460, 460, 460],
    "来源：L2 §4.3.1 表格复算。差值不是遮挡、尺度或标注问题的独立因果检验；精确原因需逐图误差分析。",
    size=39)
add("表9-复核与验收", "表 9　正式架构复核的执行与验收要求",
    "后续方案｜本次未执行训练、推理或显著性检验",
    ["步骤", "执行内容", "验收产物"],
    [
        ["1 数据与标签冻结", "共享 train / val / test 清单；来源隔离；复核框范围与 cow 类别", "manifest + 内容 hash；逐域图像数、实例数、来源簇数"],
        ["2 环境与配置冻结", "保存版本、Git commit、本地补丁、输入变换、AMP、优化器与增强", "environment / config / protocol 快照"],
        ["3 checkpoint 选择", "只用 val 选模；显式规定指标与并列规则；存 selected 权重 hash", "selection.json；逐轮 val；checkpoint SHA-256"],
        ["4 统一评估", "共用冻结 test、COCO evaluator；记录预测收集下限与 maxDets", "GT / prediction JSON；评估器版本；独立 test 结果"],
        ["5 不确定性", "确认种子真正改变训练随机流；重复训练；按来源簇 bootstrap", "训练间 SD 与样本区间分别报告"],
        ["6 结果归档", "逐域与宏平均同时展示；保存误差案例；记录耗时、峰值显存与更新次数", "逐域指标表、审计日志、可复算脚本与误差图"],
    ], [460, 910, 850],
    "依据：L2 §4.2 / §4.3；W5–W11、W13。先冻结研究问题与预算原则，再执行；不以名义 epochs 相同替代预算审计。",
    size=36)

dump(BASE / "表格清单.json", tables)
markdown = ["# 域内模型与架构比较：可编辑图表底稿",
            "", "> 来源精度按原文保留。图表与文字来自同一数据对象；更新底稿后须同步重生成。", ""]
for t in tables:
    markdown += [f"## {t['title']}", "", t["subtitle"], "",
                 "| " + " | ".join(t["headers"]) + " |",
                 "| " + " | ".join("---" for _ in t["headers"]) + " |"]
    markdown += ["| " + " | ".join(str(x).replace("\n", "<br>") for x in r) + " |"
                 for r in t["rows"]]
    markdown += ["", t["note"], ""]
for title, headers, rows in [
    ("完整 AP50 数据", ["数据集", *MODELS],
     [[k, *[str(v) for v in map50[k]]] for k in datasets]),
    ("完整固定工作点 P / R / F1", ["数据集", *MODELS],
     [[k, *[" / ".join(f"{v:.3f}" for v in cell) for cell in fixed[k]]]
      for k in datasets]),
    ("验证集最佳工作点 conf* / P / R / F1", ["数据集", *MODELS],
     [[k, *[" / ".join(f"{v:.3f}" for v in cell) for cell in best[k]]]
      for k in datasets]),
]:
    markdown += [f"## {title}", "", "| " + " | ".join(headers) + " |",
                 "| " + " | ".join("---" for _ in headers) + " |"]
    markdown += ["| " + " | ".join(r) + " |" for r in rows]
    markdown += [""]
(BASE / "表格可编辑底稿.md").write_text("\n".join(markdown), encoding="utf-8")


def diagram():
    img, d = surface(1580, "图 2　四种检测范式与本项目的比较范围",
                     "机制依据原论文与官方文档｜示意图不表示完整网络拓扑或性能排名")
    descriptions = [
        ("YOLO11m", "单阶段检测", ["图像", "多尺度特征", "检测头", "检测框"],
         "直接预测类别与边界框；本项目：640 × 640。", "W1"),
        ("RT-DETR-L", "端到端 Transformer", ["图像", "混合编码器", "查询解码器", "检测框"],
         "原生流程无需 NMS；历史自定义评测路径待核查。", "W2、W9、W10"),
        ("Faster R-CNN R50-FPN", "两阶段检测", ["图像特征", "RPN 提议", "RoI 处理", "检测框"],
         "共享特征产生候选区域，再做分类与框回归。", "W3、W12"),
        ("RetinaNet R50-FPN", "单阶段密集检测", ["图像特征", "FPN", "分类 / 回归", "检测框"],
         "Focal Loss 降低容易样本的损失贡献。", "W4、W12"),
    ]
    for i, (title, sub, blocks, note, ref) in enumerate(descriptions):
        x = M + (i % 2) * 1130
        y = 225 + (i // 2) * 590
        d.rounded_rectangle((x, y, x + 1090, y + 550), radius=20,
                            fill=LIGHT, outline=RULE, width=3)
        d.rectangle((x, y + 30, x + 9, y + 105), fill=COLORS[i])
        d.text((x + 30, y + 32), title, fill=NAVY, font=font(45, True))
        d.text((x + 30, y + 112), sub, fill=COLORS[i], font=font(37))
        for j, label in enumerate(blocks):
            xx, yy = x + 30 + j * 262, y + 240
            d.rounded_rectangle((xx, yy, xx + 238, yy + 98), radius=12,
                                fill="white", outline=COLORS[i], width=3)
            tw = font(30, True).getlength(label)
            d.text((xx + (238 - tw) / 2, yy + 25), label, fill=NAVY, font=font(30, True))
            if j < 3:
                d.line((xx + 241, yy + 49, xx + 259, yy + 49), fill=COLORS[i], width=4)
                d.polygon([(xx + 259, yy + 49), (xx + 250, yy + 42),
                           (xx + 250, yy + 56)], fill=COLORS[i])
        for n, line in enumerate(wrap(note, font(33), 1025)):
            d.text((x + 30, y + 380 + n * 49), line, fill=MUTED, font=font(33))
        d.text((x + 30, y + 493), f"依据：{ref}", fill=MUTED, font=font(29))
    save_png(img, "图2-四种检测范式")


def delta_plot():
    img, d = surface(1690, "图 3　RT-DETR-L 与 YOLO11m 的逐数据集差值",
                     "Δ=mAP50-95(RT-DETR-L)−mAP50-95(YOLO11m)｜单次历史 val 结果")
    left, right, top, row_h, xmax = 800, 2190, 302, 84, .03
    zero = (left + right) / 2
    for t in [-.03, -.02, -.01, 0, .01, .02, .03]:
        x = zero + (right - left) * t / (2 * xmax)
        d.line((x, top - 15, x, top + 14 * row_h), fill=RULE, width=2)
        d.text((x - 46, top + 14 * row_h + 18), f"{t:+.2f}", fill=MUTED, font=font(29))
    d.line((zero, top - 15, zero, top + 14 * row_h), fill=NAVY, width=3)
    for i, k in enumerate(datasets):
        y, val = top + i * row_h + 17, diff[k]
        d.text((M, y), short_name(k), fill=NAVY, font=font(35))
        xx = zero + (right - left) * val / (2 * xmax)
        color = BLUE if val > 0 else TEAL
        d.rectangle((min(zero, xx), y + 8, max(zero, xx), y + 47), fill=color)
        text = f"{val:+.4f}"
        tx = xx + 13 if val > 0 else xx - font(30, True).getlength(text) - 13
        d.text((tx, y + 6), text, fill=color, font=font(30, True))
    d.text((M, 1575), "9 域 Δ>0，5 域 Δ<0；12/14 域 |Δ|≤0.02；无多种子误差条或显著性检验。",
           fill=MUTED, font=font(33))
    save_png(img, "图3-逐数据集配对差值")


def threshold_plot():
    img, d = surface(1040, "图 4　F1 对工作点选择的敏感性",
                     "14 域等权宏平均｜固定阈值与验证集最优阈值分开报告")
    left, right, top, bottom = 290, 2270, 278, 824
    for tick in [0, .2, .4, .6, .8, 1.0]:
        y = bottom - (bottom - top) * tick
        d.line((left, y, right, y), fill=RULE, width=2)
        d.text((left - 92, y - 20), f"{tick:.1f}", fill=MUTED, font=font(31))
    fixed_display = [.893, .807, .869, .839]
    best_display = [.908, .906, .911, .894]
    for i in range(4):
        center = left + 250 + 480 * i
        for j, (val, color) in enumerate([(fixed_display[i], BLUE), (best_display[i], TEAL)]):
            x = center - 150 + 160 * j
            y = bottom - (bottom - top) * val
            d.rectangle((x, y, x + 135, bottom), fill=color)
            d.text((x - 4, y - 49), f"{val:.3f}", fill=color, font=font(33, True))
        label = MODELS[i]
        d.text((center - font(34).getlength(label)/2, bottom + 18),
               label, fill=NAVY, font=font(34))
    d.rectangle((500, 206, 528, 234), fill=BLUE)
    d.text((542, 198), "固定 conf=0.25", fill=MUTED, font=font(32))
    d.rectangle((1130, 206, 1158, 234), fill=TEAL)
    d.text((1172, 198), "各域验证集最佳 F1 工作点", fill=MUTED, font=font(32))
    d.text((M, 950), "来源：L2 §4.3.2。最优阈值在 val 上选择；该差异不证明测试部署收益或分数分布机制。",
           fill=MUTED, font=font(30))
    save_png(img, "图4-F1工作点敏感性")


diagram()
delta_plot()
threshold_plot()
source_files = [
    DRAFT, AUDIT, ROOT / "科研记录/实验记录格式参考.md",
    ROOT / "牛只数据集/10月域内重测计划.md",
    ROOT / "牛只数据集/域内重测-10月.md",
]
source_fingerprints = [
    {"path": str(p.relative_to(ROOT)).replace("\\", "/"), "bytes": p.stat().st_size,
     "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
    for p in source_files]
fingerprint_path = BASE / "本地来源校验.json"
if fingerprint_path.exists():
    assert json.loads(fingerprint_path.read_text(encoding="utf-8")) == source_fingerprints, (
        "原始来源已变化；请先审核内容变化，再显式更新复算基线。")
else:
    dump(fingerprint_path, source_fingerprints)
figures = sorted(p for p in BASE.glob("*.png") if p.stem != "图表校阅总览")
cols, thumb_w, thumb_h = 3, 760, 640
overview = Image.new("RGB", (cols * thumb_w, math.ceil(len(figures) / cols) * thumb_h), "white")
od = ImageDraw.Draw(overview)
for i, p in enumerate(figures):
    im = Image.open(p).convert("RGB")
    im.thumbnail((thumb_w - 30, thumb_h - 72))
    x, y = (i % cols) * thumb_w, (i // cols) * thumb_h
    overview.paste(im, (x + (thumb_w - im.width) // 2, y + 52))
    od.text((x + 18, y + 10), p.stem, fill=NAVY, font=font(24))
save_png(overview, "图表校阅总览")
print(json.dumps({"table_count": len(tables), "data_rows": 56,
                  "means95": means95, "means50": means50, "delta": stats["差值宏平均"],
                  "abs_delta": stats["绝对差均值"], "spearman": correlations,
                  "fixed_F1": [v[2] for v in fixed_mean],
                  "best_F1": [v[2] for v in best_mean],
                  "domain_span": stats["数据集均值跨度"],
                  "model_span": stats["模型宏平均跨度"]}, ensure_ascii=False))
