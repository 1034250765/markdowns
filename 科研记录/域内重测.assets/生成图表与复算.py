"""从本地记录摘录数据、复算并生成科研记录图表；不运行训练或修改实验源文件。"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import statistics as st
import sys
from pathlib import Path

EXTRA = Path(os.environ.get("TEMP", ".")) / "cowcv-indomain-20261014-deps"
if EXTRA.exists():
    sys.path.insert(0, str(EXTRA))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

ASSET = Path(__file__).resolve().parent
ROOT = ASSET.parent.parent
RAW = ROOT / "牛只数据集"
RECORD = RAW / "域内重测-10月.md"
LODO = RAW / "LODO测试-9月.md"
NAVY, TEAL, AMBER = "#173C53", "#348E91", "#C79540"
GRAY, PALE = "#657783", "#EEF5F6"
FONT = Path("C:/Windows/Fonts/msyh.ttc")
BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
FP = FontProperties(fname=str(FONT))
plt.rcParams.update({
    "font.family": "Microsoft YaHei", "axes.unicode_minus": False,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": NAVY, "text.color": NAVY,
    "xtick.color": GRAY, "ytick.color": GRAY,
    "font.size": 11, "figure.facecolor": "white",
})


def clean(s):
    return s.replace("**", "").replace("`", "").strip()


def section(text, heading):
    part = text.split(heading, 1)[1]
    level = len(heading) - len(heading.lstrip("#"))
    return re.split(r"\n#{1," + str(level) + r"} ", part, 1)[0]


def rows(text):
    result = []
    for line in text.splitlines():
        if line.startswith("|"):
            row = [clean(v) for v in line.strip().strip("|").split("|")]
            if not all(re.fullmatch(r"[:\-\s]+", v) for v in row):
                result.append(row)
    return result


src = RECORD.read_text(encoding="utf-8")
lodo_src = LODO.read_text(encoding="utf-8")
main_rows = rows(section(src, "### 4.2 域内结果"))
main = {}
for r in main_rows[1:]:
    if "宏平均" not in r[0]:
        main[r[0]] = dict(test_images=int(r[1]), AP50=float(r[2]), AP=float(r[3]),
                          P=float(r[4]), R=float(r[5]), repeat=r[6])
assert len(main) == 14
assert sum(d["test_images"] for d in main.values()) == 3124

selection = {}
for r in rows(section(src, "### 4.1 Checkpoint 选择"))[1:]:
    selection[r[0]] = (int(r[1]), float(r[2]))
    selection[r[4]] = (int(r[5]), float(r[6]))
assert set(selection) == set(main)

es = {}
for r in rows(section(src, "### 11.3 种子重复结果"))[1:]:
    if "宏平均" not in r[0]:
        v = [float(c) for c in r[1:4]]
        es[r[0]] = dict(values=v, reported_mean=float(r[4]), reported_SD=float(r[5]),
                        recomputed_mean=st.mean(v), recomputed_SD=st.stdev(v))
assert set(es) == set(main)

lodo = {}
for r in rows(section(lodo_src, "### 5.3 跨种子目标域对比"))[1:]:
    lodo[r[0]] = dict(values=[float(v) for v in r[2:5]],
                      reported_mean=float(r[5]), reported_SD=float(r[6]))
assert set(lodo) == set(main)

old = {}
for r in rows(section(src, "## 七、与 2026-07"))[1:]:
    if "宏平均" not in r[0]:
        name = {"Dairy Cow": "diarycow", "NWAFU": "NWAFU_CD",
                "Google": "Google_Open_Images"}.get(r[0], r[0])
        old[name] = float(r[1])
assert set(old) == set(main)

macros = {key: st.mean(v[key] for v in main.values()) for key in ("AP50", "AP", "P", "R")}
es_macros = [st.mean(v["values"][i] for v in es.values()) for i in range(3)]
lodo_macros = [st.mean(v["values"][i] for v in lodo.values()) for i in range(3)]
ratio = {t: lodo[t]["reported_mean"] / main[t]["AP"] for t in main}
noise = {
    "CBPD_ODD": [0.90809, 0.90809, 0.91641],
    "COLO": [0.65167, 0.65386, 0.65478],
    "HCRD": [0.94684, 0.94598, 0.93760],
}
calc = {
    "scope": "本地Markdown显示精度复算，不是远程原始CSV；source字段保存出处",
    "date": "2026-10-14", "source": str(RECORD), "lodo_source": str(LODO),
    "test_images_total": 3124, "domains": 14, "main_macros": macros,
    "es_macros_from_4dp": es_macros,
    "es_macro_mean_from_4dp": st.mean(es_macros),
    "es_macro_sample_SD_from_4dp": st.stdev(es_macros),
    "es_macro_reported": {"per_seed": [0.71865, 0.72153, 0.72127],
                          "mean": 0.72049, "sample_SD": 0.00159},
    "lodo_macros_from_4dp": lodo_macros,
    "lodo_macro_mean_from_4dp": st.mean(lodo_macros),
    "lodo_macro_population_SD_from_4dp": st.pstdev(lodo_macros),
    "lodo_macro_sample_SD_from_4dp": st.stdev(lodo_macros),
    "R_target_macro_from_reported_means": st.mean(ratio.values()),
    "ratio_of_AP_macros": st.mean(v["reported_mean"] for v in lodo.values()) / macros["AP"],
    "stock_noise_ranges": {t: max(v)-min(v) for t, v in noise.items()},
    "HCRD_four_run_range": 0.94684-0.92850,
    "old_macro": st.mean(old.values()),
    "AP50_AP_gap": {t: main[t]["AP50"]-main[t]["AP"] for t in main},
    "es_SD_rounding": {
        "reported_median": st.median(v["reported_SD"] for v in es.values()),
        "from_displayed_values_median": st.median(v["recomputed_SD"] for v in es.values()),
        "reported_count_le_0_004": sum(v["reported_SD"] <= 0.004 for v in es.values()),
        "recomputed_count_le_0_004": sum(v["recomputed_SD"] <= 0.004 for v in es.values()),
    },
    "selection_epochs": {t: selection[t][0] for t in main},
    "per_domain": {t: {**main[t], "selected_epoch": selection[t][0],
                        "es": es[t], "lodo": lodo[t], "R_target": ratio[t]} for t in main},
}
(ASSET / "数值复算.json").write_text(json.dumps(calc, ensure_ascii=False, indent=2), encoding="utf-8")
with (ASSET / "逐域指标与种子结果.csv").open("w", encoding="utf-8-sig", newline="") as f:
    field = ["dataset", "test_images", "selected_epoch", "AP50", "AP", "P", "R",
             "es42", "es43", "es44", "es_mean_reported", "es_SD_reported",
             "lodo42", "lodo43", "lodo44", "lodo_mean_reported", "R_target_recomputed"]
    w = csv.DictWriter(f, fieldnames=field); w.writeheader()
    for t, d in main.items():
        w.writerow(dict(dataset=t, test_images=d["test_images"], selected_epoch=selection[t][0],
                        **{k: d[k] for k in ("AP50", "AP", "P", "R")},
                        **dict(zip(["es42", "es43", "es44"], es[t]["values"])),
                        es_mean_reported=es[t]["reported_mean"], es_SD_reported=es[t]["reported_SD"],
                        **dict(zip(["lodo42", "lodo43", "lodo44"], lodo[t]["values"])),
                        lodo_mean_reported=lodo[t]["reported_mean"], R_target_recomputed=ratio[t]))

tables = []


def add_table(name, title, subtitle, headers, data, widths, notes):
    tables.append(dict(name=name, title=title, subtitle=subtitle, headers=headers,
                       rows=data, widths=widths, notes=notes))


add_table("表1-实验分工", "表 1  域内参照的证据链", "每一阶段有独立职责，test 不参与选模",
          ["阶段", "输入", "操作与产物", "证据约束"],
          [
              ["数据冻结", "data/ 与 splits/", "去重、划分；固定 14 个目标 test 视图", "按文件与清单核对；来源簇独立性另审计"],
              ["域内训练", "本域 train", "YOLO11m；100 epochs；逐轮保存", "训练池为本域全量；末批保留"],
              ["验证选模", "本域 val", "AP50–95 最大；并列较早；selected.pt", "只读取 val；第 100 轮为预定对照"],
              ["最终评测", "冻结 test", "每个预选 checkpoint 输出独立结果", "selected 与 epoch100 分别评测"],
              ["保持率分析", "同视图 LODO 三轮", "R_target = LODO 均值 / 域内主方案", "逐域比值后等权平均；保留 R > 1"],
              ["重复审计", "stock 与 es 两套运行", "分别刻画运行重复与跨 seed 离散度", "协议分开；SD 与极差分开"],
          ], [270, 360, 830, 760],
          ["依据：重测计划 §§2–7、执行记录 §§2、5、6、11；操作状态为本地历史记录转述。"])

add_table("表2-冻结训练协议", "表 2  统一训练与评测协议", "主表：stock seed=42；es 仅改变 loader 随机流",
          ["项目", "冻结设置", "核验入口 / 与 LODO 关系"],
          [
              ["检测器与类别", "YOLO11m；nc=1；cow", "同一模型；四架构不在本轮"],
              ["数据版本", "data/；SHA-256 去重；8:1:1", "25,079 / 3,142 / 3,124 图"],
              ["初始化", "lodo/yolo11m.pt", "同一权重；MD5 写入 run_info"],
              ["训练预算", "imgsz=640；100 epochs；patience=100", "固定轮数；各域优化步数不同"],
              ["批与累积", "batch=16；nbs=16；accumulate=1", "on_train_start 断言；无梯度累积"],
              ["优化器", "AdamW；lr0=0.002", "显式设置；禁止 auto"],
              ["数值设置", "AMP=True；deterministic=True", "确定性设置不等于绝对确定性保证"],
              ["末批与编译", "drop_last=False；compile=False", "末批不足 16 张也保留"],
              ["增强", "8.4.92 默认增强；close_mosaic=10", "确切默认值仍需运行 args.yaml"],
              ["保存与选模", "每轮保存剥离；val AP50–95 最大", "严格 > 扫描；并列较早"],
              ["评测", "split=test；imgsz=640；默认 evaluator", "selected / epoch100 各一行；14×2=28"],
              ["声明差异", "单域全量；stock loader；本域 val", "LODO：13 源×500；分域宏平均 val"],
              ["es 扩展", "seed→派生 generator；42/43/44", "train_es<N> 独立目录；不替换主表"],
          ], [420, 870, 930],
          ["依据：重测计划 §§3–5、11；本地 indomain_protocol.yaml、训练与评测脚本。"])

add_table("表3-完整运行时间线", "表 3  六轮完整执行与协议扩展", "时间：Asia/Shanghai；年份统一为 2026",
          ["运行名", "开始", "结束", "记录耗时", "用途"],
          [
              ["train", "10-05 15:53", "10-06 02:55", "11h01m", "stock 主方案；14/14"],
              ["train_s43", "10-06 17:50", "10-07 04:28", "10h38m", "stock 运行重复；14/14"],
              ["train_s44", "10-07 17:16", "10-08 03:56", "10h40m", "stock 运行重复；14/14"],
              ["train_es43", "10-10 13:48", "10-11 00:33", "10h45m", "有效 seed 扩展；14/14"],
              ["train_es44", "10-11 00:33", "10-11 11:08", "10h35m", "接力执行；14/14"],
              ["train_es42", "10-11 11:08", "10-11 21:55", "10h47m", "接力执行；14/14"],
          ], [480, 440, 440, 350, 510],
          ["原文耗时照录：主方案起止按分钟相减为 11h02m，与记录 11h01m 相差 1 分钟。",
           "不把六轮时长之和当完整计算成本；另含恢复、HCRD 判别与冒烟。"])

add_table("表4-域内主结果", "表 4  YOLO11m 域内监督参照", "stock seed=42 · selected.pt · frozen test · AP 数值为 0–1",
          ["目标域", "test 图", "e*", "AP50", "AP50–95", "P 默认", "R 默认"],
          [[t, str(d["test_images"]), str(selection[t][0]), f'{d["AP50"]:.4f}', f'{d["AP"]:.4f}',
            f'{d["P"]:.4f}', f'{d["R"]:.4f}'] for t, d in main.items()] +
          [["14 域等权宏平均", "3,124", "—", *[f"{macros[k]:.4f}" for k in ("AP50", "AP", "P", "R")]]],
          [610, 160, 140, 310, 330, 290, 290],
          ["依据：执行记录 §4.2；宏平均由显示的四位逐域值复算。",
           "P/R 为默认 val 的汇总工作点；不标注为 conf=0.25 严格计数。"])

add_table("表5-stock运行波动", "表 5  stock 重复的运行间波动", "11/14 域逐位一致；其余三域报告实际读数与极差",
          ["目标域", "train", "train_s43", "train_s44", "max − min"],
          [[t, *[f"{v:.5f}" for v in vals], f"{max(vals)-min(vals):.5f}"]
           for t, vals in noise.items()], [610, 400, 400, 400, 410],
          ["极差为单个正数，未写成 ±SD；三轮不能构成置信区间。",
           "依据：执行记录 §5.2；运行名中的 seed 数字不代表有效种子变化。"])

add_table("表6-HCRD同seed判别", "表 6  HCRD 同 seed 判别记录", "同 seed 重跑也发生分叉，支持存在运行间非确定性",
          ["运行", "e*", "val 峰值", "test AP50–95"],
          [["stock 主方案", "87", "0.92541", "0.94684"],
           ["stock 重复 ①", "100", "0.91925", "0.94598"],
           ["stock 重复 ②", "96", "0.92568", "0.93760"],
           ["同 seed=42 重跑", "98", "0.92888", "0.92850"]],
          [900, 230, 530, 560],
          ["四次 test 读数跨度 0.01834；不能用三轮极差替代四轮范围。",
           "依据：执行记录 §5.3；具体非确定性算子本次未定位。"])

add_table("表7-es三种子", "表 7  effective-seed 三种子扩展", "selected.pt · 同一 test 视图 · mean 与样本 SD 按原表照录",
          ["目标域", "es42", "es43", "es44", "mean", "SD (n=3)"],
          [[t, *[f"{v:.4f}" for v in d["values"]], f'{d["reported_mean"]:.4f}',
            f'{d["reported_SD"]:.4f}'] for t, d in es.items()] +
          [["14 域等权宏平均", "0.71865", "0.72153", "0.72127", "0.72049", "0.00159"]],
          [650, 310, 310, 310, 310, 340],
          ["依据：执行记录 §11.3；完整精度原始 CSV 未重取；四位输入复算有末位舍入差。",
           "跨 seed 的观测离散度可能叠加残余运行噪声；非置信区间。"])

add_table("表8-同视图LODO保持率", "表 8  同一目标 test 上的监督参照与保持率", "分母：stock 主方案；分子：LODO 三种子均值；R 不裁剪",
          ["目标域", "test 图", "域内 AP", "LODO AP", "R_target"],
          [[t, str(main[t]["test_images"]), f'{main[t]["AP"]:.4f}',
            f'{lodo[t]["reported_mean"]:.4f}', f"{ratio[t]:.3f}"]
           for t in sorted(main, key=lambda t: -ratio[t])] +
          [["14 域等权宏平均", "3,124", f'{macros["AP"]:.4f}',
            f'{st.mean(v["reported_mean"] for v in lodo.values()):.4f}', f"{st.mean(ratio.values()):.4f}"]],
          [690, 220, 420, 420, 470],
          ["R_target 宏平均是 14 个域比值的平均；两个 AP 宏平均相除为约 0.6976。",
           "依据：执行记录 §6 与 LODO 记录 §5.3；末位复算舍入差见 JSON。"])

add_table("表9-新旧描述性对照", "表 9  旧 val 与新 test 的历史对照", "数据版本、划分、优化协议、报告视图同时变化；不解释为净提升",
          ["目标域", "旧 val", "新 test", "算术差"],
          [[t, f"{old[t]:.4f}", f'{main[t]["AP"]:.4f}',
            f'{main[t]["AP"]-old[t]:+.4f}'] for t in main] +
          [["14 域等权宏平均", f"{st.mean(old.values()):.4f}", f'{macros["AP"]:.4f}',
            f'{macros["AP"]-st.mean(old.values()):+.4f}']],
          [900, 430, 430, 460],
          ["依据：执行记录 §7；该表仅描述不同历史协议的读数。",
           "CImage 差值约 −0.2763；多因素变化不能单独归因于划分或微调。"])

add_table("表10-复核与结论边界", "表 10  复核发现与采用口径", "保留原始资料，通过当前记录明确纠正与未决事项",
          ["核对项", "发现", "本记录采用口径"],
          [
              ["选模轮次", "原文概括漏掉 CID 的第 75 轮", "8-calves=63；CID=75；其余 83–100"],
              ["LODO 宏平均", "§6 将 0.734/0.729/0.735 放在 AP 描述后", "AP 三轮为约 0.5056/0.5009/0.5034；前者对应保持率"],
              ["LODO SD", "重测 §6 与 LODO §5.3 若干 SD 不同", "不混用；本文保持率表省略争议 SD"],
              ["stock 不确定性", "三轮极差被写成 ± 数值", "给原始三值及 max−min；HCRD 四轮另列"],
              ["默认 P/R", "评测脚本直接读取 results_dict", "默认 F1 峰值汇总；非固定 conf 严格计数"],
              ["预算充分性", "选模靠后被当作充分收敛依据", "预算完成已记录；充分收敛尚无证明"],
              ["随机性分量", "es 的跨 seed 差异被视为纯种子方差", "观测 SD 可叠加残余运行噪声；嵌套重复待执行"],
              ["时间记录", "主方案起止差与耗时相差 1 分钟", "照录并标注；不猜秒级时间"],
          ], [410, 870, 940],
          ["依据：本地源文档、镜像脚本与版本固定的官方源码；不是对原始日志的实时重审。"])


def font(size=38, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def wrap(text, width, f):
    out = []
    for para in str(text).split("\n"):
        line = ""
        for ch in para:
            if line and f.getlength(line + ch) > width:
                out.append(line); line = ch
            else:
                line += ch
        out.append(line)
    return out or [""]


layout_report = []


def render_table(t):
    W, M = 2400, 95
    content = W - 2*M
    widths = [int(w / sum(t["widths"]) * content) for w in t["widths"]]
    widths[-1] += content-sum(widths)
    f = font(36); hf = font(37, True)
    wrapped = [[wrap(c, w-44, f) for c, w in zip(row, widths)] for row in t["rows"]]
    heights = [max(83, max(len(v) for v in row)*49 + 31) for row in wrapped]
    header_lines = [wrap(c, w-44, hf) for c, w in zip(t["headers"], widths)]
    hh = max(95, max(len(v) for v in header_lines)*49 + 28)
    title_lines = wrap(t["title"], W-400, font(55, True))
    y0 = max(245, 105 + len(title_lines)*65 + 55)
    note_lines = [ln for n in t["notes"] for ln in wrap(n, content, font(31))]
    H = y0 + hh + sum(heights) + 66 + 44*len(note_lines)
    image = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((M, 49, M+16, 121), fill=TEAL)
    for j, line in enumerate(title_lines):
        draw.text((M+39, 49+j*65), line, fill=NAVY, font=font(55, True))
    sy = 62+len(title_lines)*65
    draw.text((M+39, sy), t["subtitle"], fill=GRAY, font=font(31))
    # Study Image 母版只在非数据区提供装饰，不参与数据行和字体生成。
    master = Image.open(ASSET / "StudyImage-科研表格视觉母版.png").convert("RGB")
    crop = master.crop((int(master.width*.90), int(master.height*.03),
                        int(master.width*.99), int(master.height*.11))).resize((125, 110))
    image.paste(crop, (W-M-125, 45))
    draw.line((M, y0, W-M, y0), fill=NAVY, width=5)
    draw.rectangle((M, y0+4, W-M, y0+hh), fill="#DDEDEF")

    def row_text(lines, top, height, use_header=False, macro=False, raw_cells=None):
        x = M
        ff = hf if use_header else (font(36, True) if macro else f)
        for k, (cell, width) in enumerate(zip(lines, widths)):
            if ff is not f:
                cell = wrap(t["headers"][k] if use_header else raw_cells[k], width-44, ff)
            y = top+(height-len(cell)*49)//2-3
            for ln in cell:
                numeric = k > 0 and bool(re.fullmatch(r"[0-9.,+−\-–—±()% =eE]+", ln))
                xx = x + width-22-ff.getlength(ln) if numeric else x+22
                assert x+8 <= xx and xx+ff.getlength(ln) <= x+width-8
                draw.text((xx, y), ln, fill=NAVY, font=ff)
                y += 49
            x += width
    row_text(header_lines, y0, hh, use_header=True)
    y = y0+hh
    for i, (row, height) in enumerate(zip(wrapped, heights)):
        macro = t["rows"][i][0] == "14 域等权宏平均"
        draw.rectangle((M, y, W-M, y+height), fill="#DDEDEF" if macro else ("#F4F8F9" if i%2==0 else "white"))
        row_text(row, y, height, macro=macro, raw_cells=t["rows"][i])
        draw.line((M, y+height, W-M, y+height), fill="#D4DFE3", width=1)
        y += height
    draw.line((M, y, W-M, y), fill=NAVY, width=3)
    y += 27
    for line in note_lines:
        draw.text((M, y), line, fill=GRAY, font=font(31)); y += 44
    assert y < H
    path = ASSET / (t["name"]+".png")
    image.save(path, dpi=(300, 300))
    layout_report.append({"file": path.name, "width": W, "height": H, "cells": sum(len(r) for r in t["rows"]),
                          "bounds_checked": True, "rendered_rows": t["rows"]})


for t in tables:
    render_table(t)
(ASSET / "表格清单.json").write_text(json.dumps(tables, ensure_ascii=False, indent=2), encoding="utf-8")
md = ["# 域内重测：表格可编辑底稿", "", "> 与正文 PNG 使用同一份数据生成；日期：2026-10-14。", ""]
for t in tables:
    md += ["## "+t["title"], "", t["subtitle"], "",
           "| "+" | ".join(t["headers"])+" |",
           "| "+" | ".join(["---"]*len(t["headers"]))+" |"]
    md += ["| "+" | ".join(r)+" |" for r in t["rows"]]
    md += ["", *["> "+n for n in t["notes"]], ""]
(ASSET / "表格可编辑底稿.md").write_text("\n".join(md), encoding="utf-8")


def savefig(fig, name, title, subtitle):
    fig.suptitle(title, fontproperties=FP, fontsize=18, x=.06, ha="left", y=.98, weight="bold", color=NAVY)
    fig.text(.06, .915, subtitle, fontproperties=FP, fontsize=10, color=GRAY)
    fig.savefig(ASSET / name, dpi=300, facecolor="white")
    plt.close(fig)


labels = list(main)
y = np.arange(14)
fig, ax = plt.subplots(figsize=(12, 7.5))
fig.subplots_adjust(left=.28, right=.94, top=.85, bottom=.1)
for i, t in enumerate(labels):
    ax.plot([main[t]["AP"], main[t]["AP50"]], [i, i], color="#B8D6D8", lw=4, zorder=1)
ax.scatter([main[t]["AP50"] for t in labels], y, color=AMBER, s=44, label="AP50", zorder=3)
ax.scatter([main[t]["AP"] for t in labels], y, color=TEAL, s=50, label="AP50–95", zorder=4)
ax.set_yticks(y, [f'{t}  (n={main[t]["test_images"]})' for t in labels])
ax.invert_yaxis(); ax.set_xlim(.38, 1.035)
ax.grid(axis="x", alpha=.18); ax.set_xlabel("AP（0–1；单类别 cow）", fontproperties=FP)
ax.legend(loc="lower right", frameon=False)
savefig(fig, "图3-域内检测与定位.png", "图 3  同一权重下的宽松检出与严格定位指标",
        "stock selected.pt；按 AP50–95 排列；连线表示指标差，不表示定位误差的唯一原因")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8), gridspec_kw={"width_ratios": [1.7, 1]})
fig.subplots_adjust(left=.25, right=.97, top=.84, bottom=.15, wspace=.55)
ordered = sorted(es, key=lambda t: es[t]["reported_SD"], reverse=True)
ax1.barh(np.arange(14), [es[t]["reported_SD"] for t in ordered],
         color=[AMBER if t=="CImage" else TEAL for t in ordered], height=.68)
ax1.set_yticks(np.arange(14), ordered); ax1.invert_yaxis()
ax1.set_xlabel("样本 SD（n=3；按原表显示精度）", fontproperties=FP)
ax1.set_xlim(0,.022); ax1.grid(axis="x", alpha=.16)
ax1.set_xticks([0,.005,.010,.015,.020], ["0.000","0.005","0.010","0.015","0.020"])
ax1.tick_params(axis="x", labelsize=9)
for i,t in enumerate(ordered):
    ax1.text(es[t]["reported_SD"]+.0003, i, f'{es[t]["reported_SD"]:.4f}', va="center", fontsize=9)
reported = [0.71865, .72153, .72127]
ax2.plot([42,43,44], reported, marker="o", lw=2, color=TEAL, label="es 宏平均")
ax2.axhline(macros["AP"], color=AMBER, ls="--", label="stock 主方案")
ax2.set_xticks([42,43,44]); ax2.set_xlim(41.65,44.35); ax2.set_ylim(.716,.724)
ax2.set_xlabel("有效 seed", fontproperties=FP)
ax2.set_ylabel("14 域等权 AP50–95", fontproperties=FP)
ax2.grid(axis="y", alpha=.16); ax2.legend(loc="lower center", fontsize=8, frameon=False)
for x,v in zip([42,43,44],reported):
    ax2.annotate(f"{v:.5f}", (x,v), xytext=(0,10), textcoords="offset points", ha="center", fontsize=9)
fig.text(.25,.05,"观察到的跨 seed 离散度可叠加残余执行噪声；误差量不是置信区间。",fontproperties=FP,fontsize=10,color=GRAY)
savefig(fig, "图4-es种子离散度.png", "图 4  effective-seed 扩展的逐域离散度与总体读数",
        "mean±SD=0.72049±0.00159；左图逐域 SD 与右图宏平均级 SD 的统计对象不同")

fig, ax = plt.subplots(figsize=(12, 8.5))
fig.subplots_adjust(left=.26, right=.88, top=.84, bottom=.11)
ordered = sorted(main, key=lambda t: -ratio[t])
for i,t in enumerate(ordered):
    a,b=main[t]["AP"], lodo[t]["reported_mean"]
    ax.plot([a,b],[i,i], color="#CCD8DE", lw=4)
    ax.scatter(a,i,color=NAVY,s=45,zorder=3)
    ax.scatter(b,i,color=TEAL,s=45,zorder=4)
    ax.text(1.01,i,f"R={ratio[t]:.3f}",va="center",fontsize=9, transform=ax.get_yaxis_transform())
ax.scatter([],[],color=NAVY,label="域内监督 stock")
ax.scatter([],[],color=TEAL,label="LODO 三种子均值")
ax.set_yticks(np.arange(14),ordered);ax.invert_yaxis()
ax.set_xlim(.08,1.0);ax.grid(axis="x",alpha=.16)
ax.set_xlabel("同一目标 test 的 AP50–95",fontproperties=FP)
ax.legend(loc="lower right",frameon=False,fontsize=9)
savefig(fig, "图5-域内与LODO配对.png", "图 5  域内监督与多源零样本在同一目标视图上的配对",
        "逐域比值宏平均约 0.7328；经验监督参照不是上限，CImage 的 R>1 如实保留")

all_figures = [ASSET / "StudyImage-域内重测证据链.png",
               ASSET / "StudyImage-随机性审计.png",
               ASSET / "图3-域内检测与定位.png",
               ASSET / "图4-es种子离散度.png",
               ASSET / "图5-域内与LODO配对.png"] + [ASSET/(t["name"]+".png") for t in tables]
thumbs = []
for path in all_figures:
    im = Image.open(path).convert("RGB")
    im.thumbnail((780, 670))
    tile = Image.new("RGB", (820, 750), "#F4F7F8")
    tile.paste(im, ((820-im.width)//2, 30))
    ImageDraw.Draw(tile).text((20,710),path.stem,fill=NAVY,font=font(23))
    thumbs.append(tile)
contact = Image.new("RGB", (820*3,750*5), "white")
for i, tile in enumerate(thumbs):
    contact.paste(tile,((i%3)*820,(i//3)*750))
contact.save(ASSET/"图表校阅总览.jpg",quality=92)
(ASSET/"图表版面检查.json").write_text(json.dumps(layout_report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in calc.items() if k not in ("per_domain","AP50_AP_gap")},
                 ensure_ascii=False,indent=2))
print(f"生成 {len(tables)} 张精确表格、3 张统计图；表格数据界限检查通过。")
