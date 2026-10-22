"""读取既有本地资料，精确排版 LODO 图表；不修改来源与正文。"""
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
LODO = ROOT / "牛只数据集/LODO测试-9月.md"
INDOMAIN = ROOT / "牛只数据集/域内重测-10月.md"
NAVY, TEAL, BLUE, GOLD = "#183A56", "#168B84", "#4B80B2", "#C18032"
MUTED, RULE, LIGHT = "#536779", "#CCD8E0", "#F0F5F8"
W, M = 2400, 90


def font(size, bold=False):
    p = "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"
    return ImageFont.truetype(p, size)


def dump(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def extract(text, marker):
    lines = text.split(marker, 1)[1].splitlines()
    found, rows = False, []
    for line in lines:
        if line.startswith("|"):
            found = True
            rows.append([v.strip().replace("**", "") for v in line.strip().strip("|").split("|")])
        elif found:
            break
    assert len(rows) > 2, marker
    return rows[0], rows[2:]


def wrap(text, f, width):
    result = []
    for paragraph in str(text).split("\n"):
        line = ""
        for token in re.findall(r"[A-Za-z0-9_]+(?:[-.][A-Za-z0-9_]+)*|\s+|.", paragraph):
            if line and f.getlength(line + token) > width:
                result.append(line.rstrip())
                line = token.lstrip()
            else:
                line += token
        result.append(line)
    assert all(f.getlength(v) <= width + 3 for v in result), result
    return result


def surface(h, title, subtitle):
    bg = Image.open(BASE / "LODO科研表格版式母图-Study-20261014.png").convert("RGB")
    bg = bg.resize((W, h))
    d = ImageDraw.Draw(bg)
    d.rectangle((28, 22, W - 28, h - 22), fill="white")
    d.rectangle((M, 54, M + 10, 117), fill=TEAL)
    d.text((M + 30, 45), title, fill=NAVY, font=font(55, True))
    d.text((M + 30, 124), subtitle, fill=MUTED, font=font(31))
    return bg, d


tables = []


def table(name, title, subtitle, headers, rows, widths, note, size=37):
    assert sum(widths) == W - 2 * M and all(len(r) == len(headers) for r in rows)
    f, hf, nf = font(size), font(size, True), font(30)
    lh = size + 17
    hl = [wrap(x, hf, widths[i] - 42) for i, x in enumerate(headers)]
    hh = max(map(len, hl)) * lh + 38
    cells = [[wrap(v, f, widths[i] - 42) for i, v in enumerate(r)] for r in rows]
    heights = [max(map(len, r)) * lh + 30 for r in cells]
    notes = wrap(note, nf, W - 2 * M)
    height = 213 + hh + sum(heights) + len(notes) * 44 + 108
    img, d = surface(height, title, subtitle)
    y, x = 209, M
    d.rectangle((M, y, W - M, y + hh), fill=LIGHT)
    d.line((M, y, W - M, y), fill=NAVY, width=4)
    for i, ls in enumerate(hl):
        for j, s in enumerate(ls):
            d.text((x + 20, y + 18 + j * lh), s, fill=NAVY, font=hf)
        x += widths[i]
    y += hh
    d.line((M, y, W - M, y), fill=NAVY, width=2)
    for ri, (row, rh) in enumerate(zip(cells, heights)):
        if ri % 2:
            d.rectangle((M, y, W - M, y + rh), fill="#F8FAFB")
        x = M
        for i, ls in enumerate(row):
            for j, s in enumerate(ls):
                d.text((x + 20, y + 14 + j * lh), s, fill=NAVY, font=f)
            x += widths[i]
        y += rh
        d.line((M, y, W - M, y), fill=RULE, width=1)
    d.line((M, y, W - M, y), fill=NAVY, width=4)
    for j, s in enumerate(notes):
        d.text((M, y + 30 + j * 44), s, fill=MUTED, font=nf)
    img.save(BASE / f"{name}.png", dpi=(300, 300))
    tables.append({"name": name, "title": title, "headers": headers, "rows": rows,
                   "width": W, "height": height, "dpi": 300, "note": note})


lodo = LODO.read_text(encoding="utf-8-sig")
indomain = INDOMAIN.read_text(encoding="utf-8-sig")
_, seed_rows = extract(lodo, "### 5.3 跨种子目标域对比")
_, id_rows = extract(indomain, "### 4.2 域内结果")
_, es_rows = extract(indomain, "### 11.3 种子重复结果")
id_data = {r[0]: {"n": int(r[1]), "map50": float(r[2]), "map95": float(r[3]),
                  "P": float(r[4]), "R": float(r[5])}
           for r in id_rows if not r[0].startswith("宏平均")}
es_data = {r[0]: [float(v) for v in r[1:4]]
           for r in es_rows if not r[0].startswith("宏平均")}
data, discrepancies = [], []
for r in seed_rows:
    name, n = r[0], int(r[1])
    vals = [float(v) for v in r[2:5]]
    mean, popsd, samplesd, rg = st.mean(vals), st.pstdev(vals), st.stdev(vals), max(vals)-min(vals)
    row = {"dataset": name, "test_images": n, "seed42": vals[0], "seed43": vals[1],
           "seed44": vals[2], "mean": mean, "population_sd": popsd, "sample_sd": samplesd,
           "range": rg, "source_mean": float(r[5]), "source_population_sd": float(r[6]),
           "source_range": float(r[7]), "indomain_stock42": id_data[name]["map95"],
           "holding_ratio": mean / id_data[name]["map95"]}
    assert id_data[name]["n"] == n
    for field, calc, src in [("mean", mean, float(r[5])), ("population_sd", popsd, float(r[6])),
                             ("range", rg, float(r[7]))]:
        if abs(calc - src) > 0.000055:
            discrepancies.append({"dataset": name, "field": field, "source": src,
                                  "recomputed_from_rounded": calc,
                                  "note": "四位逐域输入与原文汇总存在舍入差异；未改写来源"})
    data.append(row)
assert len(data) == len(id_data) == len(es_data) == 14
assert sum(r["test_images"] for r in data) == 3124
macro = [st.mean(r[f"seed{s}"] for r in data) for s in [42, 43, 44]]
correlations = {}
for a, b in combinations([42, 43, 44], 2):
    va, vb = [r[f"seed{a}"] for r in data], [r[f"seed{b}"] for r in data]
    assert len(set(va)) == len(set(vb)) == 14
    ra, rb = [sorted(va).index(v) + 1 for v in va], [sorted(vb).index(v) + 1 for v in vb]
    correlations[f"{a}-{b}"] = 1 - 6 * sum((x-y)**2 for x, y in zip(ra, rb)) / (14 * (14**2-1))
stats = {
    "input_precision": "本地逐域表四位小数，非远程全精度",
    "datasets": 14, "seed_dataset_rows": 42, "test_images": 3124,
    "seed_macro_map95": dict(zip([42,43,44], macro)),
    "macro_mean": st.mean(macro), "macro_population_sd": st.pstdev(macro),
    "macro_sample_sd": st.stdev(macro), "spearman": correlations,
    "mean_domain_population_sd": st.mean(r["population_sd"] for r in data),
    "mean_range": st.mean(r["range"] for r in data),
    "indomain_stock_macro": st.mean(v["map95"] for v in id_data.values()),
    "holding_ratio_macro_stock42": st.mean(r["holding_ratio"] for r in data),
    "ratio_of_macro_means_not_macro_holding_ratio": st.mean(macro) / st.mean(v["map95"] for v in id_data.values()),
    "es_seed_macro": {s: st.mean(v[i] for v in es_data.values()) for i,s in enumerate([42,43,44])},
    "rounded_source_discrepancies": discrepancies,
    "budget": {"lodo_epoch_steps": math.ceil(6500/16), "lodo_100epoch_steps": 40700,
               "all14_epoch_steps": math.ceil(7000/16), "all14_100epoch_steps": 43800,
               "lodo_last_batch": 4, "all14_last_batch": 8},
}
dump("LODO与域内复算-20261014.json", {"statistics": stats, "domains": data})
with (BASE / "LODO三种子与域内参照-20261014.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(data[0]))
    writer.writeheader()
    writer.writerows(data)

table("表10-研究任务与证据范围", "表 10  研究任务与证据范围",
      "同一牛只研究问题下的四类比较；历史结果、已执行测试与计划分开登记",
      ["研究任务", "训练／选模", "评测视图", "当前范围", "可回答的问题"],
      [
          ["域内四架构比较", "每域独立训练；本域 val 选模", "历史本域 val", "4×14=56 组合", "当前训练和评估配置的域内表现"],
          ["新域内监督参照", "YOLO11m 本域 train；本域 val 选模", "新 data/test", "14 域；stock＋es 扩展", "相同冻结目标视图上的监督参照"],
          ["多源 LODO", "13 源等权训练；13 源 val 宏平均选模", "留出目标 data/test", "14 fold×3 seed", "未使用目标域训练／选模信息时的表现"],
          ["外部 E 测试", "all14；14 源 val 选模", "项目外部新 E", "权重已备；E 评测待执行", "基准之外的外部有效性"],
      ], [350, 530, 320, 430, 590],
      "历史四架构 val 不与新 YOLO11m test 混表；LODO 固定一种架构，不能产生四架构跨域排名。")

table("表11-LODO冻结协议与实现", "表 11  LODO 冻结协议与实现",
      "来源：9月计划 §3.2；LODO 执行记录 §1–3（本次仅本地核对）",
      ["项目", "冻结设置／记录", "核查与解释"],
      [
          ["检测器与输入", "YOLO11m；cow；imgsz=640；AMP", "同一初始化文件；640 为参数设置，实际输入需运行产物核查"],
          ["训练与优化", "100 epochs；batch=nbs=16；AdamW；lr0=0.002", "记录断言 accumulate=1；禁止 optimizer=auto"],
          ["源域配额", "每源每 epoch 500 张；13×500=6500", "CImage 141／CBPD_ODD 292 张源图需有放回抽样"],
          ["末批与步数", "LODO：407 步／epoch，末批4张；all14：438步，末批8张", "100轮理论调用次数40700／43800；原记录断言逐轮核验"],
          ["选模", "源 val 等权宏平均 AP50–95 最高；并列较早", "selection.json＋selected.pt；stock best.pt 仅副产物"],
          ["随机性", "42／43／44；训练与抽样两层同换", "记录全14 fold重复；all14仅主方案，不进三种子汇总"],
          ["隔离与数据版本", "新划分25079／3142／3124，共31345图", "目标不参加训练与选模；精确去重不等于近重复／来源隔离完成"],
      ], [340, 950, 930],
      "LODO 与 all14 的池大小、末批大小不同；目标路径零命中只核查路径隔离，不能排除跨目录同源图像。")

table("表12-LODO三种子主结果", "表 12  LODO 三种子主结果",
      "selected.pt；目标冻结 test；AP50–95；按三种子均值降序",
      ["目标域", "图数", "seed42", "seed43", "seed44", "均值", "总体SD", "极差"],
      [[r["dataset"], str(r["test_images"]), *[f"{r[f'seed{s}']:.4f}" for s in [42,43,44]],
        f"{r['mean']:.4f}", f"{r['population_sd']:.4f}", f"{r['range']:.4f}"] for r in data]
      + [["宏平均", "3124", *[f"{v:.4f}" for v in macro], f"{st.mean(macro):.4f}",
          f"{st.pstdev(macro):.4f}", f"{max(macro)-min(macro):.4f}"]],
      [550, 140, 255, 255, 255, 255, 255, 255],
      "SD采用原记录总体标准差定义（n=3、ddof=0），不是置信区间；四位逐域值复算，少数末位与全精度汇总可能相差0.0001。",
      size=35)

ratio_rows = sorted(data, key=lambda r: r["holding_ratio"], reverse=True)
table("表13-同视图域内参照与保持率", "表 13  同视图域内参照与 LODO 保持率",
      "YOLO11m 新 data/test；域内 stock seed42 分母；LODO 三种子均值分子",
      ["目标域", "test图数", "域内监督AP", "LODO均值AP", "保持率 R"],
      [[r["dataset"], str(r["test_images"]), f"{r['indomain_stock42']:.4f}",
        f"{r['mean']:.4f}", f"{r['holding_ratio']:.4f}"] for r in ratio_rows]
      + [["14域等权宏平均", "3124", f"{stats['indomain_stock_macro']:.4f}",
          f"{stats['macro_mean']:.4f}", f"{stats['holding_ratio_macro_stock42']:.4f}"]],
      [660, 240, 440, 440, 440],
      "逐域先计算R再等权平均，不能用两个宏平均相除；监督分母不是理论上限，R允许大于1。该表不包括es或三分母×三分子组合。")

table("表14-实施问题与复核边界", "表 14  实施问题与复核边界",
      "历史工程处理、记录冲突与后续验收；不把待核实事项填成已完成",
      ["问题／证据", "已有处理或当前判断", "后续验收"],
      [
          ["持久worker与按epoch换清单", "原记录采用每epoch重建dataset＋loader", "核对各轮清单hash、实际样本名和worker流"],
          ["缓存、隐藏目录、旧split", "标签库替代逐轮cache；隐藏目录过滤；重建28个失效文件名涉及的清单", "磁盘／清单逐名与hash一致；保留旧清单"],
          ["rect验证batch不一致", "数据集分组与loader batch统一", "保存真实张量形状；不要从imgsz推断640×640"],
          ["累计清单行数", "15 fold×100轮为980万行（含all14）；14 fold训练读取910万行", "区分预生成清单量和真实LODO训练读取量"],
          ["零接触、末批与收敛措辞", "路径隔离有记录；all14末批8张；晚期峰值不足以证明收敛", "重复／来源簇审计；训练曲线及预冻结预算扩展"],
          ["P/R与test_instances", "默认val P/R不等于固定0.25计数；L5说明旧实例字段误记含目标图数", "冻结阈值另计TP/FP/FN；重导出真实实例数"],
          ["不同记录的LODO SD", "L7用总体SD；L5§6部分SD不同，不能直接合并", "核查聚合脚本、全精度输入、ddof与字段语义"],
          ["零样本与预训练来源", "未在项目中访问目标域不排除预训练时已有重叠", "COCO牛子集等逐来源审计；近重复＋采集来源复核"],
      ], [530, 910, 780],
      "以上不影响已有表格的可追溯摘录；外部E结果、四架构统一test与数据量匹配单源对照仍需实际执行。",
      size=36)
dump("LODO表格清单-20261014.json", tables)

md = ["# LODO 补充表格可编辑底稿", "", "> 整理：2026-10-14；只读来源；四位逐域值复算；正文显示科研表格图片。", ""]
for t in tables:
    md += [f"## {t['title']}", "", "| " + " | ".join(t["headers"]) + " |",
           "| " + " | ".join(["---"] * len(t["headers"])) + " |"]
    md += ["| " + " | ".join(row) + " |" for row in t["rows"]]
    md += ["", t["note"], ""]
(BASE / "LODO补充表格可编辑底稿-20261014.md").write_text("\n".join(md), encoding="utf-8")

# 数据图精确读取本地数值，横轴0–1，显示三种子原点与均值，不添加推断误差条。
img, d = surface(1750, "图 6  LODO 目标域表现与种子波动",
                 "每域显示三个运行值与均值；横线仅连接最小／最大运行值，不表示置信区间")
left, right, top, row_h = 680, 2200, 300, 84
bottom = top + 14 * row_h
for tick in [i/10 for i in range(11)]:
    x = left + (right-left)*tick
    d.line((x, top-28, x, bottom-20), fill=RULE, width=1)
    d.text((x-22, bottom+12), f"{tick:.1f}", fill=MUTED, font=font(29))
for j, (s, col) in enumerate(zip([42,43,44],[TEAL,BLUE,GOLD])):
    x = 730 + j*350
    d.ellipse((x,207,x+18,225), fill=col)
    d.text((x+32,197), f"seed={s}", fill=MUTED, font=font(32))
d.text((1800,197), "◆  三轮均值", fill=NAVY, font=font(32))
for i, r in enumerate(data):
    y = top + i*row_h
    d.text((M,y-8), r["dataset"], fill=NAVY, font=font(34))
    d.text((M+405,y-6), f"n={r['test_images']}", fill=MUTED, font=font(28))
    vals = [r[f"seed{s}"] for s in [42,43,44]]
    xs = [left+(right-left)*v for v in vals]
    d.line((min(xs),y+20,max(xs),y+20), fill=MUTED, width=4)
    for j,(x,col) in enumerate(zip(xs,[TEAL,BLUE,GOLD])):
        yy = y+20 + (j-1)*9
        d.ellipse((x-8,yy-8,x+8,yy+8), fill=col, outline="white", width=1)
    x = left+(right-left)*r["mean"]
    d.polygon([(x,y+9),(x+11,y+20),(x,y+31),(x-11,y+20)], fill=NAVY)
    d.text((2260,y-3),f"{r['mean']:.3f}", fill=NAVY,font=font(30,True))
d.text((1050,bottom+67), "目标冻结视图 AP50–95", fill=MUTED, font=font(34))
d.text((M,1600), "三轮宏平均：0.5056 / 0.5009 / 0.5034；总体SD约0.0019（n=3）", fill=NAVY,font=font(34))
d.text((M,1660), "仅作描述；跨种子离散度不替代测试样本不确定性或来源簇bootstrap。", fill=MUTED,font=font(30))
img.save(BASE / "图6-LODO种子与目标域差异.png",dpi=(300,300))

paths = [
    "牛只数据集/域内模型与架构比较.md", "牛只数据集/文章初稿.md",
    "科研记录/实验记录格式参考.md", "牛只数据集/10月域内重测计划.md",
    "牛只数据集/域内重测-10月.md", "牛只数据集/9月LODO泛化测试计划.md",
    "牛只数据集/LODO测试-9月.md",
]
dump("20261014本地来源校验.json", [
    {"path": p, "sha256": hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),
     "bytes": (ROOT/p).stat().st_size} for p in paths])

overview_paths = [BASE / "图5-域内与泛化证据链-Study原图-20261014.png",
                  *[BASE/f"{t['name']}.png" for t in tables],
                  BASE/"图6-LODO种子与目标域差异.png"]
thumbs = []
for p in overview_paths:
    im = Image.open(p).convert("RGB")
    im.thumbnail((1120,1120))
    thumbs.append((p,im))
maxh = max(im.height for _,im in thumbs)
overview = Image.new("RGB",(2400,math.ceil(len(thumbs)/2)*(maxh+80)), "#E9EFF3")
od = ImageDraw.Draw(overview)
for i,(p,im) in enumerate(thumbs):
    x,y = (i%2)*1200+40,(i//2)*(maxh+80)+60
    od.text((x,y-42),p.stem[:45],fill=NAVY,font=font(25))
    overview.paste(im,(x,y))
overview.save(BASE / "LODO图表校阅总览-20261014.png")
print(json.dumps(stats,ensure_ascii=False,indent=2))
