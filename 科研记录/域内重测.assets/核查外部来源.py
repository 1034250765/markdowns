"""只读获取官方资料与原始研究，记录访问状态、内容hash和核查片段。"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ("R1", "Ultralytics Train 官方指南", "https://docs.ultralytics.com/modes/train/", ["nbs", "deterministic", "optimizer", "close_mosaic"]),
    ("R2", "Ultralytics Val 官方指南", "https://docs.ultralytics.com/modes/val/", ["split", "conf", "iou"]),
    ("R3", "Ultralytics v8.4.92 data/build.py", "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/data/build.py", ["6148914691236517205", "seed_worker", "drop_last"]),
    ("R4", "Ultralytics v8.4.92 metrics.py", "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/utils/metrics.py", ["smooth(f1_curve", "w = [0.0", "nt_per_image"]),
    ("R5", "Ultralytics v8.4.92 trainer.py", "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/engine/trainer.py", ["accumulate =", "best_fitness == self.fitness", "init_seeds"]),
    ("R6", "PyTorch v2.5.1 Randomness", "https://raw.githubusercontent.com/pytorch/pytorch/v2.5.1/docs/source/notes/randomness.rst", ["Completely reproducible", "DataLoader", "generator"]),
    ("R7", "PyTorch v2.5.1 DataLoader 实现", "https://raw.githubusercontent.com/pytorch/pytorch/v2.5.1/torch/utils/data/dataloader.py", ["RandomSampler(dataset, generator=generator)", "_base_seed", "generator=self.generator"]),
    ("R8", "COCO 官方评估实现", "https://raw.githubusercontent.com/cocodataset/cocoapi/master/PythonAPI/pycocotools/cocoeval.py", ["iouThrs", "recThrs", "maxDets"]),
    ("R9", "Gulrajani & Lopez-Paz：DomainBed", "https://arxiv.org/abs/2007.01434", ["model selection", "Abstract", "ICLR"]),
    ("R10", "Beery et al.：Recognition in Terra Incognita", "https://arxiv.org/abs/1807.04975", ["Abstract", "location", "ECCV"]),
    ("R11", "Ultralytics v8.4.92 tasks.py", "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/nn/tasks.py", ["cls_remap", "Transferred"]),
    ("R12", "Ultralytics v8.4.92 torch_utils.py", "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/utils/torch_utils.py", ["warn_only=True", 'x["epoch"] = -1', "strip_optimizer"]),
    ("R13", "Ultralytics v8.4.92 default.yaml", "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/cfg/default.yaml", ["conf:", "iou:", "max_det:"]),
    ("R14", "Ultralytics v8.4.92 detect/train.py", "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/models/yolo/detect/train.py", ["drop_last=self.args.compile"]),
    ("R15", "Ultralytics v8.4.92 detect/val.py", "https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.92/ultralytics/models/yolo/detect/val.py", ['"target_img": np.unique(cls)', "torch.linspace(0.5, 0.95, 10)"]),
]


def fetch(spec):
    sid, title, url, keys = spec
    record = dict(id=sid, title=title, url=url)
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0 (research source verification)"})
        with urlopen(request, timeout=45) as response:
            payload = response.read()
            record.update(status=response.status, resolved_url=response.url)
        text = payload.decode("utf-8")
        if "<html" in text[:1000].lower() or "<!doctype" in text[:1000].lower():
            text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", text, flags=re.S)
            text = re.sub(r"</(?:p|div|tr|h\d|li|section)>", "\n", text)
            text = html.unescape(re.sub(r"<[^>]+>", " ", text))
            text = re.sub(r"[ \t]+", " ", text)
        matches = []
        for key in keys:
            found = list(re.finditer(re.escape(key), text, re.I))
            matches.append(dict(key=key, hits=len(found), excerpts=[
                text[max(0,m.start()-250):min(len(text),m.end()+600)] for m in found[:2]]))
        record.update(bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest(), matches=matches,
                      accessed=datetime.now(timezone(timedelta(hours=8))).isoformat())
    except Exception as exc:
        record.update(status="failed", error=str(exc))
    return record


cached_path = ROOT/"外部来源核查.json"
cached = {v["id"]: v for v in json.loads(cached_path.read_text(encoding="utf-8"))} if cached_path.exists() else {}
pending = [v for v in SOURCES if v[0] not in cached or (v[0] == "R4" and
           any(m["key"] == "weights = [" for m in cached[v[0]].get("matches", [])))]
with ThreadPoolExecutor(max_workers=6) as pool:
    fetched = {v["id"]: v for v in pool.map(fetch, pending)}
cached.update(fetched)
results = [cached[v[0]] for v in SOURCES]
(ROOT/"外部来源核查.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
for r in results:
    print(r["id"], r["status"], r["title"])
    for m in r.get("matches", []):
        print("KEY",m["key"],"HITS",m["hits"])
        for s in m["excerpts"]:
            print(s)
