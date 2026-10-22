"""核查本任务图表、来源 hash、相对链接、Wiki 元数据与 test 文档读数。"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

from PIL import Image

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
RECORD = BASE.parent / "用于测试的数据集拍摄环境与场景.md"
WIKI = ROOT / "wiki/sources/cowcv-capture-environment-scene-evidence.md"
RESULT = BASE / "复核结果.json"


def text(path):
    return path.read_text(encoding="utf-8-sig")


def slug(heading):
    heading = re.sub(r"[*`]", "", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")


def links(path):
    raw = text(path)
    problems, checked = [], 0
    for target in re.findall(r"!?\[[^\]]*\]\(([^)\n]+)\)", raw):
        if target.startswith(("https://", "http://", "mailto:")):
            continue
        rel, _, anchor = target.partition("#")
        dest = (path.parent / unquote(rel)).resolve() if rel else path
        if not dest.exists():
            problems.append(f"{path.name}: missing {target}")
            continue
        if anchor and dest.suffix == ".md":
            headings = re.findall(r"^#{1,6}\s+(.+)$", text(dest), re.M)
            slugs = {slug(h) for h in headings}
            if unquote(anchor).lower() not in slugs:
                problems.append(f"{path.name}: missing anchor {target}")
        checked += 1
    return checked, problems


def main():
    RESULT.write_text("{}", encoding="utf-8")
    checks, errors = {}, []
    checks["local_links"] = 0
    for p in [RECORD, WIKI, BASE / "表格数据.md", ROOT / "index.md"]:
        count, problems = links(p)
        checks["local_links"] += count
        errors += problems

    source_hashes = json.loads(text(BASE / "本地来源校验.json"))
    for row in source_hashes:
        digest = hashlib.sha256(Path(row["path"]).read_bytes()).hexdigest()
        if digest.lower() != row["sha256"].lower():
            errors.append("source changed: " + row["path"])
    checks["unchanged_source_hashes"] = len(source_hashes)

    data = json.loads(text(BASE / "图表数据.json"))
    md = text(BASE / "表格数据.md")
    for t in data:
        with Image.open(BASE / (t["id"] + ".png")) as im:
            if json.loads(im.info["table_data"]) != t:
                errors.append("PNG table metadata mismatch: " + t["id"])
            dpi = im.info.get("dpi", (0, 0))
            if abs(dpi[0] - 300) > 0.2 or abs(dpi[1] - 300) > 0.2:
                errors.append("DPI mismatch: " + t["id"])
        for row in [t["headers"], *t["rows"]]:
            expected = "| " + " | ".join(s.replace("\n", "<br>") for s in row) + " |"
            if expected not in md:
                errors.append("Markdown table mismatch: " + t["id"])
    checks["tables"] = len(data)
    checks["table_data_rows"] = sum(len(t["rows"]) for t in data)
    checks["table_text_png_json_agreement"] = True

    test_table = next(t for t in data if t["id"] == "表3-十月测试视图")
    n = sum(int(row[1].replace(",", "")) for row in test_table["rows"][:-1])
    assert n == 3124 == int(test_table["rows"][-1][1].replace(",", ""))
    checks["test_images_total"] = n
    checks["test_datasets"] = len(test_table["rows"]) - 1
    # 与本地 10 月记录逐成员名称对应，而不只验证自建表的合计。
    recorded = {}
    octave_table = re.search(
        r"### 4\.2[^\n]*\n(.*?)(?=\n### 4\.3)",
        text(ROOT / "牛只数据集/域内重测-10月.md"),
        re.S,
    ).group(1)
    for line in octave_table.splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*0\.\d+", line)
        if m:
            recorded.setdefault(m[1].strip(), int(m[2]))
    aliases = {"Dairy Cow（diarycow）": "diarycow"}
    for row in test_table["rows"][:-1]:
        key = aliases.get(row[0], row[0])
        assert recorded[key] == int(row[1].replace(",", "")), (key, recorded.get(key))
    checks["test_counts_match_local_october_record"] = True

    fm = text(WIKI).split("---", 2)[1]
    fields = dict(re.findall(r"^([a-z_]+):\s*([^\n]*)$", fm, re.M))
    assert all(x in fields for x in ["id", "type", "status", "created", "updated", "sources"])
    srcs = re.findall(r"^  - (.+)$", fm, re.M)
    assert len(srcs) == len(set(srcs)) == 23
    for s in srcs:
        if not s.startswith("http") and not (ROOT / s).is_file():
            errors.append("frontmatter missing source: " + s)
    checks["frontmatter_sources"] = len(srcs)
    title = re.search(r"^# (.+)$", text(WIKI), re.M).group(1)
    index = text(ROOT / "index.md")
    entries = [line for line in index.splitlines() if "cowcv-capture-environment-scene-evidence.md)" in line]
    assert len(entries) == 1
    assert f"[{title}]" in entries[0] and "| `source` | `draft` |" in entries[0]
    assert "更新：2026-10-13 | 来源：23" in entries[0]
    checks["new_index_entry_matches_frontmatter"] = True
    all_ids = []
    for p in (ROOT / "wiki").rglob("*.md"):
        raw = text(p)
        m = re.match(r"---\s*\nid:\s*([^\n]+)", raw)
        if m:
            all_ids.append(m[1].strip())
    assert len(all_ids) == len(set(all_ids))
    checks["wiki_unique_ids"] = len(all_ids)

    pngs = re.findall(r"!\[[^\]]*\]\(([^)]+\.png)\)", text(RECORD))
    assert len(pngs) == 8
    assert all(not re.match(r"^[A-Za-z]:|^/", p) for p in pngs)
    checks["body_images_relative"] = len(pngs)
    for rel in pngs:
        with Image.open(RECORD.parent / rel) as im:
            im.verify()
    with open(BASE / "scene_manifest-template.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    assert len(rows) == 1 and len(set(rows[0])) == len(rows[0])
    checks["manifest_template_fields"] = len(rows[0])
    for p in [BASE / "生成图表.py", Path(__file__).resolve()]:
        ast.parse(text(p))
    checks["python_scripts_syntax"] = True

    audit = json.loads(text(BASE / "外部来源核查.json"))
    assert len(audit["sources"]) == 15
    assert all("text" not in r for r in audit["sources"])
    checks["external_sources_listed"] = 15
    checks["external_sources_readable"] = sum(r["access_scope"] != "not_read" for r in audit["sources"])
    checks["raw_research_fulltext_not_distributed"] = True
    # 本次新增引用编号全部存在；L1-L6/格式按正文声明。
    ref_ids = set(re.findall(r"\bW(\d+)\b", text(RECORD)))
    assert ref_ids == {str(i) for i in range(1, 16)}

    result = {
        "checked_date": "2026-10-13",
        "timezone": "Asia/Shanghai",
        "status": "passed" if not errors else "failed",
        "checks": checks,
        "errors": errors,
        "not_run": ["真实图像逐图审核", "远程数据计数", "视频抽帧与相机标定", "模型训练与评估", "场景比例与统计推断", "SQLite/向量索引同步"],
    }
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
