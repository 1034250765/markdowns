"""复核来源身份、链接、Wiki索引、表格与数值，并生成可离线阅读的HTML预览。"""
from __future__ import annotations

import ast
import csv
import hashlib
import html
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

EXTRA = Path(os.environ.get("TEMP", ".")) / "cowcv-indomain-20261014-deps"
if EXTRA.exists():
    sys.path.insert(0, str(EXTRA))
import markdown
from latex2mathml.converter import convert
import yaml
from PIL import Image

ASSET = Path(__file__).resolve().parent
ROOT = ASSET.parent.parent
DOC = ASSET.parent / "域内重测.md"
WIKI = ROOT / "wiki/sources/cowcv-indomain-retest-october-evidence.md"
failures = []
checks = {}


def require(condition, message):
    if not condition:
        failures.append(message)


manifest = json.loads((ASSET/"来源hash.json").read_text(encoding="utf-8-sig"))
for item in manifest:
    p = Path(item["path"])
    require(p.exists(), f"来源不存在：{p}")
    if p.exists():
        require(hashlib.sha256(p.read_bytes()).hexdigest() == item["sha256"], f"来源内容变动：{p}")
checks["unchanged_source_hashes"] = len(manifest)

link_count = 0
for p in (DOC, WIKI, ASSET/"表格可编辑底稿.md"):
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", p.read_text(encoding="utf-8")):
        target = match.group(1).strip().strip("<>")
        if re.match(r"(https?://|mailto:|#)", target):
            continue
        resolved = (p.parent/unquote(target.split("#")[0])).resolve()
        link_count += 1
        require(resolved.exists(), f"断链：{p.name} → {target}")
checks["local_links_checked"] = link_count

txt = DOC.read_text(encoding="utf-8")
images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", txt)
require(len(images) == 15, "正文配图数应为15")
checks["body_images"] = len(images)
for target in images:
    p = DOC.parent/target
    if p.exists():
        with Image.open(p) as im:
            im.verify()
require(len(re.findall(r"^## [1-7]\.", txt, re.M)) == 7, "缺少七项实验记录结构")
require(txt.startswith("# 域内重测\n"), "标题不一致")

def metadata(p):
    text = p.read_text(encoding="utf-8")
    require(text.startswith("---\n"), f"缺少Frontmatter：{p}")
    if not text.startswith("---\n"):
        return {}, ""
    front = yaml.safe_load(text.split("---",2)[1])
    heading = re.search(r"^# (.+)$",text,re.M)
    return front, heading.group(1) if heading else ""

index = (ROOT/"index.md").read_text(encoding="utf-8")
index_matches = re.findall(r"^- \[([^\]]+)\]\(([^)]+)\) \| `([^`]+)` \| `([^`]+)` \| 更新：(\S+) \| 来源：(\d+) — (.+)$",
                           index,re.M)
indexed_paths = [m[1] for m in index_matches]
require(len(indexed_paths) == len(set(indexed_paths)), "索引重复路径")
section_names = ["来源摘要","概念与方法","实体","对比","综合分析"]
type_for_section = dict(zip(section_names,["source","concept","entity","comparison","synthesis"]))
ids = {}
for p in (ROOT/"wiki").rglob("*.md"):
    if p.name == "AGENTS.md":
        continue
    data, title = metadata(p)
    required = {"id","type","status","created","updated","sources"}
    require(required <= set(data), f"Wiki元数据缺失：{p.name}")
    identity = data.get("id")
    require(identity not in ids, f"Wiki ID重复：{identity}")
    ids[identity] = p
for title,target,kind,status,updated,n_sources,desc in index_matches:
    p = ROOT/target
    require(p.exists(), f"索引目标不存在：{target}")
    if not p.exists():
        continue
    data, h1 = metadata(p)
    require(title == h1, f"索引标题不一致：{target}")
    require(kind == data.get("type") and status == data.get("status"), f"索引类型状态不一致：{target}")
    require(updated == str(data.get("updated")), f"索引更新日期不一致：{target}")
    require(int(n_sources) == len(set(data.get("sources",[]))), f"来源数不一致：{target}")
    pos = index.index(f"]({target})")
    headings = list(re.finditer(r"^## (.+)$",index[:pos],re.M))
    require(headings and type_for_section.get(headings[-1][1]) == kind, f"索引章节错误：{target}")
for section_name in section_names:
    part = index.split(f"## {section_name}",1)[1].split("\n## ",1)[0]
    titles = re.findall(r"^- \[([^\]]+)\]",part,re.M)
    require(titles == sorted(titles), f"索引标题未升序：{section_name}")
new_meta,_ = metadata(WIKI)
require(len(set(new_meta["sources"])) == 26, "新来源数应为26")
for source in new_meta["sources"]:
    if re.match(r"https?://", source):
        continue
    p = Path(source) if Path(source).is_absolute() else ROOT/source
    require(p.exists(),f"Wiki来源路径不存在：{source}")
checks.update(wiki_unique_ids=len(ids), index_entries_checked=len(index_matches), new_page_sources=26)

tables = json.loads((ASSET/"表格清单.json").read_text(encoding="utf-8"))
layout = json.loads((ASSET/"图表版面检查.json").read_text(encoding="utf-8"))
require(len(tables) == 10 and len(layout) == 10, "表格应有10张")
for spec, draw in zip(tables, layout):
    require(spec["rows"] == draw["rendered_rows"], f"排字行不一致：{spec['name']}")
    require(draw["bounds_checked"], f"界限检查未通过：{spec['name']}")
    p = ASSET/(spec["name"]+".png")
    require(p.exists(), f"缺少表格PNG：{p.name}")
    with Image.open(p) as im:
        require(im.width == 2400, f"表格宽度不正确：{p.name}")
checks["exact_tables"] = len(tables)
calc = json.loads((ASSET/"数值复算.json").read_text(encoding="utf-8"))
require(calc["test_images_total"] == 3124 and calc["domains"] == 14, "数据规模不匹配")
require(abs(calc["main_macros"]["AP"]-.7214)<1e-10, "AP宏平均不匹配")
require(abs(calc["R_target_macro_from_reported_means"]-.7327588405372948)<1e-9, "R宏平均不匹配")
require(calc["selection_epochs"]["CID"] == 75, "CID轮次不正确")
csv_rows = list(csv.DictReader((ASSET/"逐域指标与种子结果.csv").open(encoding="utf-8-sig",newline="")))
require(len(csv_rows) == 14 and sum(int(v["test_images"]) for v in csv_rows)==3124,"派生CSV规模不匹配")
for v in csv_rows:
    require(float(v["AP"]) == calc["per_domain"][v["dataset"]]["AP"],"CSV与复算不一致")
checks.update(domains=14, test_images=3124, csv_rows=14, numeric_recalculation=True)
external = json.loads((ASSET/"外部来源核查.json").read_text(encoding="utf-8"))
require(len(external)==15 and all(v["status"]==200 for v in external), "外部来源有访问失败")
checks["external_primary_sources_verified"] = len(external)
for p in ASSET.glob("*.py"):
    ast.parse(p.read_text(encoding="utf-8"), filename=p.name)
checks["python_syntax_checked"] = len(list(ASSET.glob("*.py")))

# 防止Markdown解析破坏公式下标；转换为本地MathML，不依赖远程脚本。
math_chunks = []
def block_math(match):
    latex = match.group(1).strip().replace(r"\operatorname*", r"\operatorname")
    math_chunks.append(convert(latex, display="block"))
    return f'\n\n<div class="equation">{math_chunks[-1]}</div>\n\n'
protected = re.sub(r"\$\$(.*?)\$\$", block_math, txt, flags=re.S)
def inline_math(match):
    math_chunks.append(convert(match.group(1).strip(), display="inline"))
    return math_chunks[-1]
protected = re.sub(r"(?<!\$)\$([^$\n]+)\$(?!\$)", inline_math, protected)
body = markdown.markdown(protected, extensions=["fenced_code","tables","sane_lists"])
body = re.sub(r"<p><em>((?:图|表) .*?)</em></p>", r'<p class="caption"><em>\1</em></p>', body, flags=re.S)
css = """
:root{--navy:#173c53;--teal:#348e91;--ink:#243746;--gray:#677b89;}
*{box-sizing:border-box}
body{margin:0;background:#eaf0f2;color:var(--ink);font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif;font-size:16px;line-height:1.92}
main{max-width:1000px;margin:36px auto;padding:60px 78px 80px;background:white;box-shadow:0 10px 42px #25404d14}
h1{font-size:44px;letter-spacing:.12em;margin:0 0 25px;color:var(--navy);border-bottom:4px solid var(--teal);padding-bottom:15px}
h2{font-size:24px;margin:52px 0 20px;padding:9px 0 9px 18px;border-left:5px solid var(--teal);background:#f3f7f8;color:var(--navy)}
h3{font-size:19px;margin:28px 0 12px;color:var(--navy)}
p{margin:14px 0;text-align:justify}
blockquote{margin:22px 0;padding:15px 22px;background:#f4f8f9;border-left:3px solid #8bb8bd;color:#425b6c}
blockquote p{margin:4px 0;font-size:14px}
img{display:block;max-width:100%;height:auto;margin:24px auto 8px}
img[src*="StudyImage-域内重测"],img[src*="StudyImage-随机性"]{max-width:650px}
p.caption{font-size:13px;line-height:1.65;color:var(--gray);text-align:left;margin:0 0 24px}
li{margin:8px 0}
a{color:#267b8c;text-decoration:none;border-bottom:1px solid #b5d2d7;overflow-wrap:anywhere}
pre{background:#f1f5f7;border:1px solid #dde6ea;padding:18px 22px;border-radius:4px;overflow-x:auto;line-height:1.6;font-size:13px}
code{font-family:Consolas,"Microsoft YaHei",monospace;overflow-wrap:anywhere}
strong{color:var(--navy)}
hr{border:0;border-top:1px solid #ccdbe1;margin:38px 0}
.equation{overflow-x:auto;padding:14px 0;margin:16px 0}
math{font-size:1.05em}
@media(max-width:800px){main{margin:0;padding:30px 22px}h1{font-size:36px}h2{font-size:21px}}
@media print{body{background:white;font-size:10pt;line-height:1.72}main{max-width:none;margin:0;padding:0;box-shadow:none}h1{font-size:25pt}h2{font-size:15pt;break-after:avoid}h3{font-size:12pt;break-after:avoid}img{max-height:235mm;object-fit:contain;break-inside:avoid}pre,.equation{break-inside:avoid}a{color:inherit;border:0}blockquote{break-inside:avoid}@page{size:A4;margin:18mm 16mm}}
"""
page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="../"><title>域内重测 · 科研记录</title><style>'+css+'</style></head><body><main>'+body+'</main></body></html>'
(ASSET/"阅读预览.html").write_text(page,encoding="utf-8")
checks["offline_mathml_formulas"] = len(math_chunks)
checks["html_preview"] = "阅读预览.html"
checks["markdown_characters"] = len(txt)
checks["failures"] = failures
(ASSET/"核验结果.json").write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(checks,ensure_ascii=False,indent=2))
if failures:
    raise SystemExit(1)
