"""检查本任务文件、相对链接、索引、来源身份与图表数据。"""
import ast
import csv
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote

from PIL import Image

ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parents[1]
REPORT = ROOT / "科研记录/三种模型测试.md"
WIKI = ROOT / "wiki/sources/cowcv-three-model-test-evidence.md"
INDEX = ROOT / "index.md"
checks, errors = {}, []

link_count = 0
for path in (REPORT, WIKI, INDEX, ASSETS / "表格可编辑底稿.md"):
    content = path.read_text(encoding="utf-8-sig")
    content = re.sub(r"```.*?```", "", content, flags=re.S)
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content):
        if re.match(r"[a-zA-Z]+://", target) or target.startswith("#"):
            continue
        target = unquote(target.split("#")[0].split("?")[0].strip("<>"))
        resolved = (path.parent / target).resolve()
        # 自己正在生成的核验文件，待全部检查结束再写。
        if resolved == ASSETS / "文件与数值核验.json":
            link_count += 1
            continue
        if not resolved.exists():
            errors.append(f"断链：{path.relative_to(ROOT)} -> {target}")
        link_count += 1
checks["local_markdown_links_checked"] = link_count

record_text = REPORT.read_text(encoding="utf-8")
images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", record_text)
assert len(images) == 13
for target in images:
    with Image.open(REPORT.parent / target) as image:
        assert image.width == 2400
        assert abs(image.info.get("dpi", (0, 0))[0] - 300) < 1
checks["body_images"] = {"count": 13, "figures": 5, "tables": 8,
                        "width_px": 2400, "dpi": 300}

fm = re.match(r"\A---\n(.*?)\n---", WIKI.read_text(encoding="utf-8"), flags=re.S).group(1)
for field in ("id", "type", "status", "created", "updated", "sources"):
    assert re.search(rf"^{field}:", fm, flags=re.M), field
sources = re.findall(r"^  - (.+)$", fm, flags=re.M)
assert len(sources) == len(set(sources)) == 15
for source in sources:
    if not source.startswith("https://"):
        assert (ROOT / source).is_file(), source
wiki_text = WIKI.read_text(encoding="utf-8")
title = re.search(r"^# (.+)$", wiki_text, flags=re.M).group(1)
index_text = INDEX.read_text(encoding="utf-8")
wiki_rel = WIKI.relative_to(ROOT).as_posix()
entry = re.findall(rf"^- .*{re.escape(wiki_rel)}.*$", index_text, flags=re.M)
assert len(entry) == 1 and f"[{title}]" in entry[0]
assert "| `source` | `draft` | 更新：2026-10-14 | 来源：15" in entry[0]
assert len(re.findall(re.escape(wiki_rel), index_text)) == 1
source_section = index_text.split("## 来源摘要")[1].split("## 概念与方法")[0]
section_titles = re.findall(r"^- \[(.*?)\]", source_section, flags=re.M)
assert section_titles == sorted(section_titles)
wiki_ids = []
for path in (ROOT / "wiki").rglob("*.md"):
    contents = path.read_text(encoding="utf-8-sig")
    id_match = re.search(r"^id:\s*(.+)$", contents, flags=re.M)
    if id_match:
        wiki_ids.append(id_match.group(1))
assert len(wiki_ids) == len(set(wiki_ids))
checks["wiki_index"] = {"required_fields": "pass", "unique_sources": 15,
                        "entry_consistency": "pass", "section_order": "pass",
                        "unique_wiki_ids": len(wiki_ids)}

hashes = json.loads((ASSETS / "来源文件hash.json").read_text(encoding="utf-8"))
for item in hashes:
    assert hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest() == item["sha256"]
checks["unchanged_local_source_hashes"] = len(hashes)

records = json.loads((ASSETS / "逐数据集读数.json").read_text(encoding="utf-8"))
with (ASSETS / "逐数据集读数.csv").open(encoding="utf-8-sig", newline="") as stream:
    csv_rows = list(csv.DictReader(stream))
assert len(records) == len(csv_rows) == 42
assert len({(r["dataset"], r["model"]) for r in records}) == 42
for row, csv_row in zip(records, csv_rows):
    for key, value in row.items():
        assert csv_row[key] == ("" if value is None else str(value))
checks["machine_data"] = {"unique_model_dataset_pairs": 42, "csv_json_agree": True}

tables = json.loads((ASSETS / "表格结构数据.json").read_text(encoding="utf-8"))
data_table = next(t for t in tables if t["number"] == 3)
for row in data_table["rows"]:
    n = row[0]
    for model, col in (("YOLO11s", 2), ("YOLO11l", 3), ("RetinaNet", 4)):
        r = next(r for r in records if r["dataset"] == n and r["model"] == model)
        assert Decimal(row[col]) == Decimal(str(r["map5095"]))
stats = json.loads((ASSETS / "统计复算.json").read_text(encoding="utf-8"))
expected = {"YOLO11s": "0.7406", "YOLO11l": "0.7448", "RetinaNet": "0.7001"}
for model, expected_ap in expected.items():
    source_values = [Decimal(str(r["map5095"])) for r in records if r["model"] == model]
    mean_ap = sum(source_values) / 14
    assert f"{mean_ap:.4f}" == expected_ap
assert stats["counts"]["yolo_eval_images"] == 4971 - 1023 - 560 + 2131 + 420
assert stats["yolo_l_minus_s"]["wins"] == 9
assert not json.loads((ASSETS / "排版测量.json").read_text(encoding="utf-8"))["cell_overflow_errors"]
checks["data_tables_and_arithmetic"] = "pass"

external = json.loads((ASSETS / "外部来源核查.json").read_text(encoding="utf-8"))
checks["external_sources"] = [{"id": r["id"], "status": r["status"]} for r in external]
for item in external:
    if item.get("http_status") != 200:
        errors.append(f"外部来源未完成：{item['id']} {item['status']}")
for path in ASSETS.glob("*.py"):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
checks["python_syntax"] = "pass"
checks["visual_review"] = "目视查看图表总览、表3、表7及图5；未见文字裁切和数据区域重叠"
checks["not_run"] = ["远程训练", "推理", "历史checkpoint身份核查", "成员级重复审计复现",
                     "多seed统计显著性", "SQLite与向量索引同步"]
checks["errors"] = errors
checks["status"] = "pass" if not errors else "partial"
(ASSETS / "文件与数值核验.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(checks, ensure_ascii=False, indent=2))
assert not errors, errors
