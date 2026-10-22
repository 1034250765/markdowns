"""核对新记录、派生数据、相对链接和知识库元数据，不修改原始资料。"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import re
import statistics as st
from pathlib import Path
from urllib.parse import unquote

from PIL import Image

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
RECORD = BASE.parent / "多源留一域泛化.md"
WIKI = ROOT / "wiki/sources/cowcv-indomain-architecture-evidence.md"
text = RECORD.read_text(encoding="utf-8")
wiki = WIKI.read_text(encoding="utf-8")
data = json.loads((BASE / "图表数据.json").read_text(encoding="utf-8"))
tables = json.loads((BASE / "表格清单.json").read_text(encoding="utf-8"))
new_tables = json.loads((BASE / "LODO表格清单-20261014.json").read_text(encoding="utf-8"))
new_data = json.loads((BASE / "LODO与域内复算-20261014.json").read_text(encoding="utf-8"))
stats = json.loads((BASE / "数值复算.json").read_text(encoding="utf-8"))
local_links, external_links = [], set()
for p in [RECORD, WIKI, BASE / "表格可编辑底稿.md", BASE / "LODO补充表格可编辑底稿-20261014.md"]:
    content = p.read_text(encoding="utf-8")
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content):
        if target.startswith(("https://", "http://")):
            external_links.add(target)
            continue
        path_part, _, anchor = target.partition("#")
        dst = (p.parent / unquote(path_part)).resolve()
        if dst not in [BASE / "核验结果.json", BASE / "20261014核验结果.json"]:
            assert dst.is_file(), f"断链：{p.name}: {target}"
        assert not Path(path_part).is_absolute(), f"非相对内部链接：{target}"
        if anchor:
            assert dst.suffix == ".md"
        local_links.append({"file": str(p.relative_to(ROOT)), "target": target})

images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
assert len(images) == 20
assert [int(v) for v in re.findall(r"\*表 (\d+)", text)] == list(range(1, 15))
assert [int(v) for v in re.findall(r"\*图 (\d+)", text)] == list(range(1, 7))
assert len(tables) == 9 and len(new_tables) == 5
for table in tables + new_tables:
    with Image.open(BASE / f"{table['name']}.png") as im:
        assert im.size == (2400, table["height"])
        assert abs(im.info["dpi"][0] - 300) < .1
    assert all(len(row) == len(table["headers"]) for row in table["rows"])
for image in images:
    with Image.open((RECORD.parent / image).resolve()) as im:
        im.verify()

for table_index, key, precision in [
    (3, "best_map_epoch", "epoch"), (4, "map95", "map"), (5, "fixed_prf", "F1")
]:
    table = tables[table_index]
    assert len(table["rows"]) == 14
    for i, dataset in enumerate(data["datasets"]):
        vals = data[key][dataset]
        cells = table["rows"][i][1:]
        for j in range(4):
            expected = vals[j][2] if precision == "F1" else vals[j]
            assert float(cells[j]) == expected

counts = tables[0]["rows"]
totals = [0, 0, 0, 0]
for row in counts[:-1]:
    numbers = [0 if x == "-" else int(x.replace(",", "")) for x in row[1:]]
    assert sum(numbers[:3]) == numbers[3]
    totals = [x+y for x, y in zip(totals, numbers)]
assert totals == [23851, 4971, 2551, 31373]
assert totals == [int(v.replace(",", "")) for v in counts[-1][1:]]

with (BASE / "逐模型逐数据集指标.csv").open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 56
assert len({(r["dataset"], r["model"]) for r in rows}) == 56
for r in rows:
    dataset, i = r["dataset"], data["models"].index(r["model"])
    assert r["split"] == "val"
    assert float(r["map50_95"]) == data["map95"][dataset][i]
    assert float(r["map50"]) == data["map50"][dataset][i]
    for j, field in enumerate(["P@0.25", "R@0.25", "F1@0.25"]):
        assert float(r[field]) == data["fixed_prf"][dataset][i][j]
    for j, field in enumerate(["conf_best", "P_best", "R_best", "F1_best"]):
        assert float(r[field]) == data["best_thr_prf"][dataset][i][j]
    assert int(r["map_peak_epoch"]) == data["best_map_epoch"][dataset][i]

front = wiki.split("---", 2)[1]
fields = dict(re.findall(r"^([a-z]+):\s*(.+)$", front, re.M))
for key in ["id", "type", "status", "created", "updated"]:
    assert key in fields
assert fields["id"] == "cowcv-indomain-architecture-evidence"
assert fields["type"] == "source" and fields["status"] == "draft"
sources = re.findall(r"^  - (.+)$", front, re.M)
assert len(sources) == len(set(sources)) == 24
for source in sources:
    if not source.startswith("https://"):
        assert (ROOT / source).is_file()
ids = {}
for p in (ROOT / "wiki").rglob("*.md"):
    match = re.search(r"^id:\s*(.+)$", p.read_text(encoding="utf-8-sig"), re.M)
    if match:
        page_id = match.group(1)
        assert page_id not in ids, f"重复 ID: {page_id}"
        ids[page_id] = str(p.relative_to(ROOT))
index = (ROOT / "index.md").read_text(encoding="utf-8-sig")
target = "wiki/sources/cowcv-indomain-architecture-evidence.md"
assert index.count(target) == 1
entry = next(line for line in index.splitlines() if target in line)
title = re.search(r"^# (.+)$", wiki, re.M).group(1)
assert f"[{title}]" in entry
assert "| `source` | `draft` | 更新：2026-10-14 | 来源：24" in entry
source_section = index.split("## 来源摘要", 1)[1].split("\n## ", 1)[0]
titles = re.findall(r"^- \[([^\]]+)\]", source_section, re.M)
assert titles == sorted(titles)
assert "label-studio-annotation-workflow-evidence.md" in index
assert "cowcv-dataset-test-evaluation-evidence.md" in index

hashes = json.loads((BASE / "20261014本地来源校验.json").read_text(encoding="utf-8"))
for row in hashes:
    assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]
ast.parse((BASE / "生成图表与复算.py").read_text(encoding="utf-8"))
ast.parse((BASE / "补充LODO图表与复算-20261014.py").read_text(encoding="utf-8"))
ast.parse(Path(__file__).read_text(encoding="utf-8"))
assert stats["RT领先域数"] == 9 and stats["YOLO领先域数"] == 5
assert stats["绝对差不超过0.02的域数"] == 12
assert len(re.findall(r"^## [1-7]\.", text, re.M)) == 7
assert len(re.findall(r"^\- \*\*W\d+", text, re.M)) == 17
assert len(re.findall(r"^\- \*\*L\d+", text, re.M)) == 7
assert text.count("$$") % 2 == 0 and text.count("```") % 2 == 0
official = json.loads((BASE / "官方来源核查.json").read_text(encoding="utf-8"))
assert len(official) == 14 and all(item["status"] == "opened" for item in official)
new_official = json.loads((BASE / "20261014外部来源核查.json").read_text(encoding="utf-8"))
assert len(new_official["sources"]) == 17 and all(item["status"] == "opened" for item in new_official["sources"])
assert len(new_official["image_generation"]) == 2
domains, new_stats = new_data["domains"], new_data["statistics"]
assert len(domains) == 14 and sum(r["test_images"] for r in domains) == 3124
assert len({r["dataset"] for r in domains}) == 14
with (BASE / "LODO三种子与域内参照-20261014.csv").open(encoding="utf-8-sig", newline="") as f:
    new_csv = list(csv.DictReader(f))
assert len(new_csv) == 14
for row, csv_row, table_row in zip(domains, new_csv, new_tables[2]["rows"]):
    assert row["dataset"] == csv_row["dataset"] == table_row[0]
    vals = [row[f"seed{s}"] for s in [42,43,44]]
    assert math.isclose(row["mean"], st.mean(vals))
    assert math.isclose(row["population_sd"], st.pstdev(vals))
    assert math.isclose(row["sample_sd"], st.stdev(vals))
    assert math.isclose(row["holding_ratio"], st.mean(vals) / row["indomain_stock42"])
    for field in ["seed42", "seed43", "seed44", "mean", "population_sd", "sample_sd", "holding_ratio"]:
        assert math.isclose(float(csv_row[field]), row[field])
    assert [f"{v:.4f}" for v in vals] == table_row[2:5]
    assert f"{row['mean']:.4f}" == table_row[5]
    assert f"{row['population_sd']:.4f}" == table_row[6]
    assert f"{row['range']:.4f}" == table_row[7]
ratios = {r["dataset"]: r for r in domains}
for row in new_tables[3]["rows"][:-1]:
    source = ratios[row[0]]
    assert int(row[1]) == source["test_images"]
    assert row[2] == f"{source['indomain_stock42']:.4f}"
    assert row[3] == f"{source['mean']:.4f}"
    assert row[4] == f"{source['holding_ratio']:.4f}"
assert f"{new_stats['macro_mean']:.4f}" == "0.5033"
assert f"{new_stats['indomain_stock_macro']:.4f}" == "0.7214"
assert f"{new_stats['holding_ratio_macro_stock42']:.4f}" == "0.7328"
assert new_stats["budget"]["lodo_last_batch"] == 4
assert new_stats["budget"]["all14_last_batch"] == 8
assert min(new_stats["spearman"].values()) > .9912
for name in ["YOLO11m", "RT-DETR-L", "Faster R-CNN", "RetinaNet"]:
    i = data["models"].index(name)
    assert math.isclose(st.mean(v[i] for v in data["map95"].values()), stats["mAP50-95宏平均"][i])
report = {
    "status": "passed",
    "date": "2026-10-14", "record_sections": 7, "record_images": 20, "scientific_tables": 14,
    "local_link_occurrences": len(local_links), "external_reference_urls": len(external_links),
    "datasets": 14, "model_dataset_rows": 56, "image_counts": totals,
    "sources": 24, "official_sources_opened": 17,
    "lodo_seed_dataset_rows": 42, "new_test_images": 3124,
    "lodo_macro_mean": new_stats["macro_mean"], "holding_ratio_macro": new_stats["holding_ratio_macro_stock42"],
    "source_hashes_unchanged": len(hashes), "wiki_unique_ids_checked": len(ids),
    "index_entry": entry, "source_title_sorting": "passed",
    "csv_and_table_numeric_consistency": "passed", "python_syntax": "passed",
    "visual_review": "已查看历史及新增图表总览、Study Image新证据链和新增关键表格与种子图；无裁切或数据区域重叠",
    "not_run": ["远程训练与推理", "远程产物当前存在性", "历史安装源码与checkpoint身份复核",
                "逐图误差审核", "显著性检验", "数据库与向量索引同步"],
}
(BASE / "20261014核验结果.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False))
