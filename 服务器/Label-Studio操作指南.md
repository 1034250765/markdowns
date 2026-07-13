# Label Studio 操作指南

> 手动管理 LS 用手册。以 **yxli 实例**（1.23，测试/个人用）为主线，youw 实例（1.21，正式标注，已停）列参数表。所有命令的实际参数已填好，可直接复制执行。
>
> 维护原则：实例参数变了改本文件对应行；流程/坑相对稳定。

---

## 0. 两套实例参数（权威）

机器：`211.69.141.71`（A100 工作站，CentOS 7），SSH 端口 55522，用户 yxli。

| 项 | yxli 实例（主线） | youw 实例（已停，要用再拉起） |
|----|------|------|
| LS 版本 | 1.23.0（Python 3.10） | 1.21.0（Python 3.11） |
| 端口 | 8080 | 8081 |
| SSH 别名 | `211.69.141.71` | `youw-a100` |
| 登录账号 | `chuxiao` / `103425` | 9 账号，主 `1034250765` |
| conda 环境 | `/data1/yxli/miniconda3/envs/label-studio` | `/home/youw/softwares/miniconda3` |
| DATA_DIR | `/data1/yxli/label-studio-data` | `/home/youw/.local/share/label-studio` |
| sqlite3 | `<DATA_DIR>/label_studio.sqlite3` | 同左 |
| DOCUMENT_ROOT | `/data1/yxli/ls-test` | `/data2/youw/database/CowsDatabases`（软链 `/data2/youw/database`） |
| 启动方式 | tmux 会话 `ls` + `start_ls.sh` | Python 启动器 `_launch_ls.py` |
| 启动脚本 | `/data1/yxli/label-studio-data/start_ls.sh` | `/data1/youw/_launch_ls.py` |
| 监听 host | 127.0.0.1（仅隧道） | 0.0.0.0 |
| local-files 要求 | 环境变量 **+** UI 建 Local Storage 连接 | 仅环境变量 |
| 当前状态 | ✅ 运行中 | ⏸ 已停（2026-07-12） |

**访问都靠 SSH 隧道**（防火墙未放行端口）：
```bash
# 本地终端开隧道（yxli）
ssh -N -L 8080:localhost:8080 211.69.141.71
# 浏览器打开
http://localhost:8080/
```
本地端口被占就换：`-L 9090:localhost:8080` → 访问 `localhost:9090`。

---

## 1. 启动 / 重启 / 停止

### 核心原则
- LS 是长服务，必须**脱离终端**运行（tmux 会话内前台跑）
- **改环境变量必须重启才生效**
- 同机两实例共用 `pkill -f "label-studio"` 会全杀，**必须带 `--port` 区分**

### start_ls.sh 内容（yxli，已存在）
`/data1/yxli/label-studio-data/start_ls.sh`：
```bash
#!/bin/bash
source /data1/yxli/miniconda3/etc/profile.d/conda.sh
conda activate label-studio
cd /data1/yxli/label-studio-data

# local-files 协议: 让 /data/local-files/?d=xxx 读到 /data1/yxli/ls-test/xxx
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/data1/yxli/ls-test

exec label-studio start \
  --host 127.0.0.1 \
  --port 8080 \
  --username chuxiao \
  --password 103425 \
  --data-dir /data1/yxli/label-studio-data \
  --log-level INFO \
  -b
```

### 操作命令（SSH 进服务器后）

```bash
# 看会话在不在
tmux ls                      # 应有 ls 会话

# 首次创建（如果没 ls 会话）
tmux new -d -s ls
tmux send-keys -t ls 'bash /data1/yxli/label-studio-data/start_ls.sh' Enter

# 重启
tmux send-keys -t ls C-c                                            # 停
tmux send-keys -t ls 'bash /data1/yxli/label-studio-data/start_ls.sh' Enter  # 启

# 看实时日志（不开 tmux 也能看）
tmux capture-pane -t ls -p | tail -30

# 进入会话（Ctrl+B 然后 D 脱离，任务继续跑）
tmux attach -t ls

# 销毁会话
tmux kill-session -t ls
```

### 停止（按端口区分，别误杀 8081）
```bash
pkill -f "label-studio start.*--port 8080"
```

### 验证启动
```bash
curl -sS -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:8080/
# 200 或 302 = 正常；Django 启动慢，最多等 30s
```

### 不会开机自启
服务器重启后 LS 不会自动起，要手动 `tmux send-keys ... start_ls.sh`。

### youw 实例拉起（已停，要用时）
```bash
ssh_execute(host="youw-a100", command="/home/youw/softwares/miniconda3/bin/python /data1/youw/_launch_ls.py")
```

---

## 2. local-files 协议（图片不显示排障）

> 图片不显示（前端报 "URL scheme/CORS"、后端 404/403）几乎都是这个协议没配对。

### 原理
LS 后端通过 `/data/local-files/` 接口把本地图片传给前端。task 的 image 字段写成：
```
/data/local-files/?d=<相对 DOCUMENT_ROOT 的路径>/xxx.jpg
```
后端按 `d=` 的相对路径在 `DOCUMENT_ROOT` 下定位文件。接口**默认关、有权限校验**。

### 两个必须的环境变量（已写进 start_ls.sh，缺一不可）
| 变量 | 值 | 说明 |
|------|----|----|
| `LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED` | `true` | 总开关，默认 false |
| `LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT` | `/data1/yxli/ls-test` | 图片根，`d=` 相对此路径 |

- ❌ `LABEL_STUDIO_LOCAL_FILES_SERVING_DIR` 是假变量，别用
- ❌ LS 1.23 CLI 不支持 `--allow-serving-local-files`（报错），用环境变量

### 现象 → 根因 → 解法（看后端状态码）
| 后端状态 | 根因 | 解法 |
|---------|------|------|
| 403 | `LOCAL_FILES_SERVING_ENABLED` 没设/false | 设 `=true`，重启 LS |
| 401 | 设了变量但没登录 | 登录后再看（401 = 正常） |
| 404 | 路径不属于已注册的 LocalFilesImportStorage（**1.23 特有**） | UI 建 Local Storage 连接（见 §3） |
| 200 | 正常 | - |

**1.23 的 404 根因**：源码校验请求路径必须属于某个已注册的 `LocalFilesImportStorage` 记录。手动 JSON 拼的 URL 没对应 storage 记录 → 404。**所以 1.23 光设环境变量不够，必须在 UI 建 Local Storage 连接**。

### 验证排障
```bash
# 1. 确认环境变量进了进程
cat /proc/$(pgrep -f "label-studio start.*--port 8080")/environ | tr '\0' '\n' | grep LOCAL_FILES

# 2. 后端实际状态码（未登录 401 正常）
curl -sS -o /dev/null -w "%{http_code}\n" "http://127.0.0.1:8080/data/local-files/?d=cid_predict/xxx.jpg"

# 3. 确认文件存在
ls /data1/yxli/ls-test/<相对路径>/xxx.jpg
```

---

## 3. 建项目 + 导入图片 + 预标注（✅ 正确流程）

> **顺序最重要**：① 建项目 ② 建 Local Storage 连接（只注册，**不要 Sync**！）③ JSON 导入 task（带 image URL + predictions）

### 步骤一：建项目

**UI 建项目**（推荐）：登录 → Create Project → 填名字 → Save。自动设 organization_id，无坑。

**Django shell 手动建**（API 走不通时）：⚠️ `Project.objects.create(title=...)` 默认 `organization_id=None` → **孤儿项目，DB 有记录但 UI 列表不显示**！必须显式设 organization_id（可见性决定字段）+ created_by_id。

```python
exec("""
from projects.models import Project
from organizations.models import Organization
org = Organization.objects.first()          # 通常 id=1
p = Project.objects.create(title='新项目名', organization=org, created_by_id=1)
print('created project id=%d org=%s' % (p.id, p.organization_id))
""")
```

**已建成孤儿的修复**（sqlite3 直改，LS 按请求查库，不用重启立即生效）：
```bash
sqlite3 /data1/yxli/label-studio-data/label_studio.sqlite3 \
  "UPDATE project SET organization_id=1, created_by_id=1 WHERE id=<PID>;"
```
排查：`SELECT id,title,created_by_id,organization_id FROM project;` —— organization_id 为空的就是孤儿。

### 步骤二：设 label config
项目 → Settings → Labeling Interface，填：
```xml
<View>
  <Image name="image" value="$image"/>
  <RectangleLabels name="label" toName="image">
    <Label value="Cow"/>
  </RectangleLabels>
</View>
```
- `value="$image"` ↔ task data 的 `image` 字段
- `name="label"` `toName="image"` ↔ prediction 的 `from_name`/`to_name`
- `<Label value="Cow"/>` ↔ prediction 的 `rectanglelabels: ["Cow"]`

> 手动建项目时 `update_label_config()` 多行 XML 也触发 InteractiveConsole 语法错，可直接 sqlite3 写（XML 单行无换行）：
> ```bash
> sqlite3 <DATA_DIR>/label_studio.sqlite3 "UPDATE project SET label_config='<View>...</View>' WHERE id=<PID>;"
> ```

### 步骤三：建 Local Storage 连接（只保存，不要 Sync！）
项目 → Settings → Cloud Storage → Add Source Storage：
| 字段 | 值 |
|------|----|
| Storage type | **Local files** |
| Path | `<DOCUMENT_ROOT 的子目录>`，如 `cid_predict` ⚠️ **不能等于 DOCUMENT_ROOT 本身** |

→ **Save**。到此为止，**不要点 Sync Storage**。

> 也可 ORM 建：`LocalFilesImportStorage.objects.create(path='cid_predict', project=p, title='...')`，path 必须是 DOCUMENT_ROOT 子目录。

### 步骤四：JSON 导入 task（带 image + predictions）

**方式 A（UI，小批量）**：项目页 → Import → 上传 JSON 文件

**方式 B（Django shell 手动建 Task+Prediction，大批量 >1000 最稳）**：

LS 1.23 没有公开的 `import_tasks` 函数（`tasks.functions` 里没有），直接 ORM 批量建 + 刷计数：

```python
exec("""
import json
from projects.models import Project
from tasks.models import Task, Prediction
from django.db import transaction
p = Project.objects.get(id=<PID>)
with open('<JSON_PATH>') as f:
    tasks_data = json.load(f)
ct = cp = 0
with transaction.atomic():
    for td in tasks_data:
        t = Task.objects.create(project=p, data=td['data'])
        ct += 1
        for pred in td.get('predictions', []):
            Prediction.objects.create(task=t, project=p, result=pred.get('result', []), score=pred.get('score', 1.0))
            cp += 1
print('created tasks=%d predictions=%d' % (ct, cp))
from tasks.functions import update_tasks_counters
update_tasks_counters(Task.objects.filter(project=p), from_scratch=True)
print('after tasks=%d preds=%d' % (Task.objects.filter(project=p).count(), Prediction.objects.filter(task__project=p).count()))
""")
```
- `update_tasks_counters(..., from_scratch=True)` **必调**，否则 UI 显示数量不对
- 2056 task 约 30 秒
- exec 包裹的原因见 §7 的 InteractiveConsole 坑

### JSON 结构（带 YOLO 预标注）
```json
[
  {
    "data": {"image": "/data/local-files/?d=cid_predict/xxx.jpg"},
    "predictions": [{
      "result": [{
        "type": "rectanglelabels",
        "value": {
          "x": 21.388, "y": 34.12, "width": 49.90, "height": 65.58,
          "rotation": 0, "rectanglelabels": ["Cow"]
        },
        "to_name": "image", "from_name": "label", "image_rotation": 0,
        "original_width": 800, "original_height": 450
      }],
      "score": 1.0
    }]
  },
  { "data": {"image": "/data/local-files/?d=cid_predict/no_label.jpg"} }
]
```
- 没标注的图只写 `data`，不写 `predictions`（空 task）
- `value.x/y/width/height`：**百分比 0-100，左上角坐标系**（转换见 §5）
- `original_width/height`：图片真实像素（PIL 读）

### ❌ 千万别点 Local Storage 的 Sync Storage
Sync 扫图片目录造的 task 有两个致命问题：
1. data key 是 `$undefined$`（不是 `image`），图片不显示
2. 不带 predictions

**Sync = 造坏副本**。误点了就查 `$undefined$` key 删掉（见 §6）。

### predictions vs annotations
| 字段 | 含义 | task 状态 |
|------|------|----------|
| `predictions` | 预标注（模型先标，人工确认） | 仍 unlabeled，Submit 才完成 |
| `annotations` | 已完成标注 | completed |

YOLO 自动标注走 `predictions`；纯人工标注不写这俩字段，直接 UI 标。

---

## 4. 数据查询（sqlite3 直查，只读）

```bash
# 进 sqlite3
sqlite3 /data1/yxli/label-studio-data/label_studio.sqlite3
```

### 关键表
| 表 | 含义 |
|----|------|
| `task` | 任务（每条 = 一张图） |
| `task_completion` | 标注（人工完成的） |
| `prediction` | 预标注 |
| `htx_user` | 用户（不是 auth_user） |
| `project` | 项目 |
| `io_storages_localfilesimportstorage` + `...link` | Local Storage 连接 + task 关联 |

### 常用查询
```sql
-- 各项目 task 数 + 预标注数
SELECT t.project_id, COUNT(t.id) AS tasks, COUNT(p.id) AS preds
FROM task t LEFT JOIN prediction p ON p.task_id=t.id
GROUP BY t.project_id;

-- 列出所有项目（看 organization_id 是否为空 → 孤儿）
SELECT id, title, created_by_id, organization_id FROM project ORDER BY id;

-- 看 task 的 data key（image 正常 / $undefined$ 坏副本）
SELECT id, data FROM task WHERE project_id=<PID> LIMIT 5;

-- 统计好坏副本 + 预标注分布
SELECT
  CASE WHEN json_extract(t.data,'$.image') IS NOT NULL THEN 'image'
       WHEN json_extract(t.data,'$.$undefined$') IS NOT NULL THEN 'undefined'
       ELSE '?' END AS key,
  COUNT(*) AS n,
  SUM(CASE WHEN p.id IS NOT NULL THEN 1 ELSE 0 END) AS preds
FROM task t LEFT JOIN prediction p ON p.task_id=t.id
WHERE t.project_id=<PID> GROUP BY key;

-- 看已完成的标注
SELECT c.task_id, json_extract(t.data,'$.image') AS img
FROM task_completion c JOIN task t ON t.id=c.task_id
WHERE c.project_id=<PID>;

-- 列出用户
SELECT id, username, email FROM htx_user;
```

---

## 5. YOLO ↔ LS 格式转换

### 坐标体系差异
| 体系 | 原点 | 坐标值 | 含义 |
|------|------|--------|------|
| YOLO | 左上角 | 归一化 0-1 | center x, y, width, height |
| LS | 左上角 | 百分比 0-100 | 左上角 x, y, width, height |

### YOLO → LS
```
x      = (cx - w/2) * 100
y      = (cy - h/2) * 100
width  = w * 100
height = h * 100
```
### LS → YOLO
```
cx = (x + width/2) / 100
cy = (y + height/2) / 100
w  = width / 100
h  = height / 100
```

### 转换脚本：YOLO → LS predictions JSON
扫描图片目录 + YOLO 标注目录，生成 LS 导入用 JSON。改参数即用：

```python
#!/usr/bin/env python3
"""YOLO 标注 -> Label Studio predictions JSON"""
import os, json, glob
from PIL import Image

# ============ 参数（按需修改）============
IMG_DIR   = "/data1/yxli/ls-test/cid_predict"   # 图片目录
LABEL_DIR = "/data1/yxli/new_labels/CID_predict/labels"  # YOLO 标注目录(.txt)
CLASS_MAP = {0: "Cow"}                          # YOLO class id -> LS 标签名
IMG_REL   = "cid_predict"                       # ?d= 后子路径(相对 DOCUMENT_ROOT)
OUTPUT    = "/data1/yxli/ls-test/cid-predictions.json"
CLAMP     = True                                # 越界坐标裁剪到 0-100
# ========================================

tasks, n_pred, n_empty, clamped = [], 0, 0, 0
for img_path in sorted(glob.glob(os.path.join(IMG_DIR, "*.jpg"))):
    name = os.path.basename(img_path)
    stem = os.path.splitext(name)[0]
    with Image.open(img_path) as im:
        w, h = im.size
    url = f"/data/local-files/?d={IMG_REL}/{name}"
    task = {"data": {"image": url}}
    results = []
    label_path = os.path.join(LABEL_DIR, stem + ".txt")
    if os.path.exists(label_path):
        for line in open(label_path):
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            cls = int(parts[0]); cx, cy, bw, bh = map(float, parts[1:5])
            x, y = (cx - bw/2) * 100, (cy - bh/2) * 100
            width, height = bw * 100, bh * 100
            if CLAMP:
                if x<0 or y<0 or x+width>100 or y+height>100: clamped += 1
                x = max(0, min(100, x)); y = max(0, min(100, y))
                width = max(0, min(100-x, width)); height = max(0, min(100-y, height))
            results.append({
                "type": "rectanglelabels",
                "value": {"x": round(x,4), "y": round(y,4), "width": round(width,4),
                          "height": round(height,4), "rotation": 0,
                          "rectanglelabels": [CLASS_MAP.get(cls, str(cls))]},
                "to_name": "image", "from_name": "label", "image_rotation": 0,
                "original_width": w, "original_height": h,
            })
    if results:
        task["predictions"] = [{"result": results, "score": 1.0}]; n_pred += 1
    else:
        n_empty += 1
    tasks.append(task)
json.dump(tasks, open(OUTPUT, "w"), ensure_ascii=False, indent=2)
print(f"tasks: {len(tasks)}  with_pred: {n_pred}  empty: {n_empty}  clamped: {clamped}  -> {OUTPUT}")
```

### class 映射注意
- YOLO class id（0,1,2...）和 LS label 名（"Cow"）是两套体系，必须显式映射
- 漏映射的类丢框；建议转换前对齐 YOLO classes.txt ↔ LS label config `<Label value>`

---

## 6. 数据清理（API 走不通时）

### 为什么 API 走不通（LS 1.23）
- legacy token 被禁：`"legacy token authentication has been disabled"`
- Basic auth 被禁：401
- JWT 端点本地无明文

改用 Django shell 走 ORM 或 sqlite3 直删。

### Django shell（推荐，级联安全）
```bash
# 必须 --data-dir，否则连到默认空库 ~/.labelstudiodata
label-studio shell --data-dir /data1/yxli/label-studio-data < /tmp/op.py
```

⚠️ **InteractiveConsole 多行块语法错（最大坑）**：`label-studio shell` 对顶层多行块（if/else、for、with、def、try）解析有问题，常在最后一行报 `SyntaxError: invalid syntax`，前面代码可能没执行。**不是空行问题**，写文件再重定向也躲不掉。

**通用解法：用 `exec("...")` 包裹整个脚本**（InteractiveConsole 看到单行语句，多行块在 exec 字符串里正常解析）：

```python
exec("""
from projects.models import Project
from tasks.models import Task
from django.db import transaction
with transaction.atomic():
    n, detail = Task.objects.filter(project_id=<PID>, data__icontains='$undefined$').delete()
    print('deleted %d %s' % (n, detail))
print('remaining %d' % Task.objects.filter(project_id=<PID>).count())
""")
```

**写文件用 Python 而非 heredoc**（heredoc 里 `"""` 引号冲突会截断）：
```bash
python -c "open('/tmp/op.py','w').write('exec(\"\"\"...\"\"\")')"
```

### sqlite3 直删（最快，手动级联）
按 FK 依赖顺序删，**顺序不能错**：
```sql
DELETE FROM tasks_annotationdraft   WHERE task_id IN (SELECT id FROM task WHERE project_id=<PID> AND json_extract(data,'$.$undefined$') IS NOT NULL);
DELETE FROM task_comment_authors    WHERE task_id IN (SELECT id FROM task WHERE project_id=<PID> AND json_extract(data,'$.$undefined$') IS NOT NULL);
DELETE FROM tasks_tasklock          WHERE task_id IN (SELECT id FROM task WHERE project_id=<PID> AND json_extract(data,'$.$undefined$') IS NOT NULL);
DELETE FROM prediction              WHERE task_id IN (SELECT id FROM task WHERE project_id=<PID> AND json_extract(data,'$.$undefined$') IS NOT NULL);
DELETE FROM io_storages_localfilesimportstoragelink WHERE task_id IN (SELECT id FROM task WHERE project_id=<PID> AND json_extract(data,'$.$undefined$') IS NOT NULL);
DELETE FROM task WHERE project_id=<PID> AND json_extract(data,'$.$undefined$') IS NOT NULL;
```
删后刷新计数：Django shell `Project.objects.get(id=<PID>).update_task_states()`，或**重启 LS** 最干净。

### 删前备份
```bash
cp /data1/yxli/label-studio-data/label_studio.sqlite3 \
   /data1/yxli/label-studio-data/label_studio.sqlite3.bak.$(date +%H%M)
```

### 重置密码
```python
exec("""
from django.contrib.auth import get_user_model
U = get_user_model()
u = U.objects.get(username='chuxiao')
u.set_password('新密码')
u.save()
print('done')
""")
```

### 路径迁移（数据集搬家后）
DB 里 Local Storage 的 path 是旧路径 → 图片失效。解法**建软链接**指向新位置：
```bash
ln -s <新实际路径> <DB里记录的旧路径的父目录>
```
⚠️ 别误删此软链，否则图片又 404；不要靠 Sync 修复（Sync 造坏副本）。

---

## 7. 导出标注

项目页 → Export → 选格式：

| 格式 | 用途 |
|------|------|
| JSON | LS 原生，含完整 task + annotation |
| JSONL | 每行一个 task，便于流处理 |
| COCO | 检测训练（images/annotations JSON） |
| YOLO | 检测训练（labels/*.txt + images/） |

导出后可直接喂训练。也可后台导出到 `<DATA_DIR>/export/`。

### LS 导出 JSON → YOLO（反向）
```python
import json, os
INPUT = "project-export.json"; OUT_DIR = "labels"; LABEL_MAP = {"Cow": 0}
os.makedirs(OUT_DIR, exist_ok=True)
for item in json.load(open(INPUT)):
    name = item["data"]["image"].split("/")[-1]
    stem = os.path.splitext(name)[0]
    lines = []
    for ann in item.get("annotations", []):
        for r in ann.get("result", []):
            if r.get("type") != "rectanglelabels": continue
            v = r["value"]; cls = LABEL_MAP.get(v["rectanglelabels"][0])
            if cls is None: continue
            x, y, w, h = v["x"], v["y"], v["width"], v["height"]
            lines.append(f"{cls} {(x+w/2)/100:.6f} {(y+h/2)/100:.6f} {w/100:.6f} {h/100:.6f}")
    open(os.path.join(OUT_DIR, stem+".txt"), "w").write("\n".join(lines))
```

---

## 8. 核心坑速查（6 个最容易踩）

1. **Local Storage 只注册不 Sync**：Sync 造 `$undefined$` key 的坏 task（图片不显示、无预标注）。正确顺序：先建 Local Storage 连接（保存即可）→ 再 JSON 导入。

2. **local-files 两个环境变量缺一不可**：`LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true`（默认 false）+ `LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/data1/yxli/ls-test`。改完必须重启。`LABEL_STUDIO_LOCAL_FILES_SERVING_DIR` 是假变量。

3. **手动建项目必须设 `organization_id`**：`Project.objects.create(title=...)` 默认 None → 孤儿项目 UI 不可见。必须显式设 organization_id（通常 1）+ created_by_id。修复：`UPDATE project SET organization_id=1, created_by_id=1 WHERE id=<PID>`，不用重启。

4. **Django shell 多行块用 exec 包裹**：`label-studio shell` 的 InteractiveConsole 对顶层 if/for/with/try 报 SyntaxError。用 `exec("...")` 包整个脚本绕过。写文件用 Python 而非 heredoc。

5. **LS 1.23 API 走不通**：legacy token/Basic auth 禁用。查改数据用 Django shell 或 sqlite3 直查。`--data-dir` 必须带，否则连错库。

6. **`$undefined$` 是坏副本标志**：task data key 应是 label config 字段名（如 `image`）。查到 `$undefined$` = Local Storage Sync 造的坏 task，删后重导。

---

## 9. 常用命令速查

```bash
# === 启停 ===
tmux send-keys -t ls C-c                                    # 停
tmux send-keys -t ls 'bash /data1/yxli/label-studio-data/start_ls.sh' Enter  # 启
tmux capture-pane -t ls -p | tail -30                       # 看日志
curl -sS -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:8080/  # 验证

# === 隧道（本地）===
ssh -N -L 8080:localhost:8080 211.69.141.71

# === 查状态 ===
sqlite3 /data1/yxli/label-studio-data/label_studio.sqlite3 \
  "SELECT p.id,p.title,(SELECT COUNT(*) FROM task t WHERE t.project_id=p.id) FROM project p ORDER BY p.id;"

# === Django shell ===
label-studio shell --data-dir /data1/yxli/label-studio-data < /tmp/op.py
# (脚本内容用 exec("""...""") 包裹)

# === 备份 ===
cp /data1/yxli/label-studio-data/label_studio.sqlite3{,.bak.$(date +%H%M)}

# === 环境变量检查 ===
cat /proc/$(pgrep -f "label-studio start.*--port 8080")/environ | tr '\0' '\n' | grep LOCAL_FILES
```

---

## 10. 当前状态快照（2026-07-12）

**yxli 8080（运行中）**：
| id | title | tasks | predictions | 说明 |
|----|-------|-------|------------|------|
| 2 | cow_cv | 60 | 52 | 测试集，`/data1/yxli/ls-test/` |
| 6 | CID_predict | 2056 | 2056 | YOLO 预标注单类 Cow，`/data1/yxli/ls-test/cid_predict/` |

**youw 8081**：已停，6 项目 6818 task，要用再拉起。

**DB 备份**：`/data1/yxli/label-studio-data/label_studio.sqlite3.bak.1255`（yxli 稳定后可清）
