"""检查本次产物结构与可复核性；不修改原始资料、索引或日志。"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import Counter
from urllib.parse import unquote
import ast
import hashlib
import json
import re
import sys
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DOC = HERE.parent / "27个牛类公开数据集详细档案.md"
WIKI = ROOT / "wiki/sources/cattle27-public-dataset-evidence.md"
data = json.loads((HERE / "档案与图表数据.json").read_text(encoding="utf-8"))
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

def slug(title):
    return re.sub(r"[^\w\s-]", "", title.lower()).strip().replace(" ", "-")

checked_links = []
for path in [DOC, WIKI, HERE / "表格可编辑底稿.md"]:
    text = path.read_text(encoding="utf-8")
    for raw in re.findall(r"!?\[[^\]]*\]\((<[^>]+>|[^)\n]+)\)", text):
        target = raw.strip("<>")
        if re.match(r"^[a-zA-Z]+://", target):
            continue
        relative, _, anchor = target.partition("#")
        resolved = (path.parent / unquote(relative)).resolve() if relative else path
        check(resolved.exists(), f"链接不存在：{path.name} -> {target}")
        if anchor and resolved.exists() and resolved.suffix == ".md":
            body = resolved.read_text(encoding="utf-8")
            anchors = set(re.findall(r'<a id="([^"]+)"', body))
            anchors |= {slug(h) for h in re.findall(r"^#{1,6}\s+(.+)$", body, re.M)}
            check(anchor in anchors, f"锚点不存在：{target}")
        checked_links.append({"from":str(path.relative_to(ROOT)),"target":target})

document = DOC.read_text(encoding="utf-8")
ids = re.findall(r"^#### [A-E]\d+\..+〔总表编号 (\d+)〕",document,re.M)
check(sorted(map(int,ids))==list(range(1,28)),"正文卡片编号不是 01–27 唯一集合")
check(len(data["datasets"])==27,"JSON 数据集数量错误")
check(sum(n for _,n in data["modality_counts"])==27,"模态统计合计错误")
actual = Counter(d["modality"] for d in data["datasets"])
rgb_count = sum(n for m,n in actual.items() if m in {"RGB","RGB（双目相机）"})
check(rgb_count==17 and actual["RGB-D"]==5 and actual["RGB＋热成像"]==2,"主要模态计数与实际条目不同")
check(502*450==225900,"CVB 名义帧数计算错误")
check(656+14==670 and 1886+62==1948,"Aerial Pasture 分母计算错误")
check(83+294==377 and 7*560==3920,"README 图数或同步视角图数计算错误")

tables = []
for t in data["tables"]:
    im = Image.open(HERE/t["filename"])
    check(json.loads(im.info["table_data"])==t,f"{t['id']} PNG 元数据与 JSON 不同")
    check(im.width==2600,f"{t['id']} 图片宽度错误")
    check(all(abs(v-300)<1 for v in im.info.get("dpi",[])),f"{t['id']} 缺少 300 dpi 元数据")
    check(len(t["rows"])>0,f"{t['id']} 空表")
    tables.append({"id":t["id"],"rows":len(t["rows"]),"image":t["filename"],"pixels":im.size})
check(len(tables)==10,"表格数量错误")
images=re.findall(r"!\[[^\]]*\]\(([^)]+)\)",document)
check(len(images)==13,"正文应有 3 图＋10 表")
check(all(not re.match(r"^(?:[A-Za-z]:|/|file:)",img) for img in images),"正文存在绝对图片路径")
for image in images:
    im=Image.open(DOC.parent/image)
    im.verify()

hashes=[]
for row in json.loads((HERE/"本地来源校验.json").read_text(encoding="utf-8")):
    value=hashlib.sha256((ROOT/row["path"]).read_bytes()).hexdigest()
    check(value==row["sha256"],f"来源文件已变化：{row['path']}")
    hashes.append({"path":row["path"],"unchanged":value==row["sha256"]})

wiki_text=WIKI.read_text(encoding="utf-8")
front=wiki_text.split("---",2)[1]
for key in ["id","type","status","created","updated","sources"]:
    check(re.search(rf"^{key}:",front,re.M) is not None,f"Frontmatter 缺少 {key}")
sources=re.findall(r"^  - (.+)$",front,re.M)
check(len(set(sources))==28,"来源摘要去重来源数不是 28")
wiki_ids=[]
for p in (ROOT/"wiki").rglob("*.md"):
    m=re.search(r"^id:\s*(.+)$",p.read_text(encoding="utf-8"),re.M)
    if m:
        wiki_ids.append(m.group(1))
check(len(wiki_ids)==len(set(wiki_ids)),"Wiki 页面 ID 重复")
index=(ROOT/"index.md").read_text(encoding="utf-8")
title=re.search(r"^# (.+)$",wiki_text,re.M).group(1)
entries=[line for line in index.splitlines() if "wiki/sources/cattle27-public-dataset-evidence.md" in line]
check(len(entries)==1,"新来源摘要索引条目重复或缺失")
if entries:
    check(title in entries[0] and "| `source` | `draft` | 更新：2026-10-13 | 来源：28" in entries[0],"索引与 Frontmatter 不一致")
for section in index.split("## ")[1:]:
    titles=re.findall(r"^- \[([^\]]+)\]",section,re.M)
    check(titles==sorted(titles),"索引章节内标题不是升序")
for p in HERE.glob("*.py"):
    ast.parse(p.read_text(encoding="utf-8"))

report={
    "checked_at":datetime.now(timezone(timedelta(hours=8))).isoformat(),
    "result":"passed" if not errors else "failed",
    "dataset_cards":len(ids),
    "tables":tables,
    "table_total_rows":sum(t["rows"] for t in tables),
    "document_images":len(images),
    "checked_local_links":len(checked_links),
    "local_links":checked_links,
    "local_source_hashes":hashes,
    "wiki_sources":len(set(sources)),
    "wiki_id_unique":len(wiki_ids)==len(set(wiki_ids)),
    "index_entry_unique":len(entries)==1,
    "visual_qa":"已人工查看原示意、表格母版、全部表格总览和重点放大图；修改文字换行和图片标签坐标后再次查看。",
    "not_run":["全量数据包下载与解压","原图逐图审查","原包标签转换","数据包级重复审计","实际分组划分","远程状态核查","模型训练与评估","统计显著性检验","SQLite/Qdrant/向量索引同步"],
    "errors":errors,
}
(HERE/"复核结果.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k in {"result","dataset_cards","table_total_rows","document_images","checked_local_links","wiki_sources","errors"}},ensure_ascii=False))
if errors:
    raise SystemExit(1)
