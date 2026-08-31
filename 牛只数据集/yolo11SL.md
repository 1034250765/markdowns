# YOLO11s/YOLO11l 牛只数据集训练与测试过程及结果

## 1. 实验概况

| 项目 | 内容 |
|---|---|
| 任务 | 单类别牛只目标检测，类别名为 `cow`，类别 ID 为 `0` |
| 模型 | YOLO11s、YOLO11l |
| 检测框架 | Ultralytics 8.4.92 |
| 运行环境 | Python 3.10.18，PyTorch 2.5.1+cu124，CUDA 12.4 |
| GPU | NVIDIA A100-PCIE-40GB |
| 数据集数量 | 14 个 |
| 训练状态 | YOLO11s：14/14；YOLO11l：14/14，均完成 100 epochs |
| 评估状态 | YOLO11s：14/14；YOLO11l：14/14 |
| 服务器 | `yxli@211.69.141.71:55522` |
| 项目根目录 | `/data1/yxli/CODE/ultralytics/self_mAP` |

本实验沿用项目中已经准备好的数据集视图和划分，不重新随机划分、不修改原始图片和标签。
`Cows2021` 和 `diarycow` 使用已有的 `test` 划分；其余 12 个数据集使用已有的 `val`
划分。因此，后者的结果是同域验证结果，不能表述为独立测试集结果。

## 2. 训练流程

### 2.1 项目脚本与目录

训练和评估均在远程项目中执行：

```text
/data1/yxli/CODE/ultralytics/self_mAP/
├── configs/                         # 14 个数据集 YAML 配置
├── datasets/                        # 已准备好的 images/labels 视图
├── models/
│   ├── yolo11s.pt
│   └── yolo11l.pt
├── scripts/
│   ├── check_yolo11s.py             # YOLO11s 只读预检
│   ├── check_yolo11l.py             # YOLO11l 只读预检
│   ├── train_yolo11s.py             # 单数据集训练入口
│   ├── train_yolo11l.py             # 单数据集训练入口
│   ├── run_yolo11s_all.sh           # YOLO11s 14 集串行队列
│   ├── run_yolo11l_all.sh           # YOLO11l 14 集串行队列
│   ├── evaluate_yolo11s.py          # YOLO11s val/test 评估
│   ├── evaluate_yolo11l.py          # YOLO11l val/test 评估
│   ├── summarize_yolo11s.py         # YOLO11s 汇总
│   └── summarize_yolo11l.py         # YOLO11l 汇总
├── outputs/
│   ├── yolo11s/<run>/               # 训练结果和 checkpoint
│   ├── yolo11l/<run>/               # 训练结果和 checkpoint
│   └── evaluations/                 # val/test 评估结果
└── logs/
    ├── yolo11s_14/                 # YOLO11s 日志和汇总
    └── yolo11l_14/                 # YOLO11l 日志和汇总
```

### 2.2 数据准备与只读预检

每个数据集都有对应的 `configs/<dataset>.yaml` 和 `datasets/<dataset>/`。训练脚本通过
配置文件读取已有的 `train`、`val`、`test` 目录，不调用随机划分逻辑。

正式训练前分别执行 `check_yolo11s.py` 和 `check_yolo11l.py`，预检内容包括：

1. YAML 配置和各 split 目录是否存在；
2. 图片和标签是否能够配对；
3. 标签是否全部为单类别 `0 cow`；
4. 图片数量是否与既定数量一致；
5. `Cows2021` 和 `diarycow` 的 `test` 目录是否存在。

14 个数据集均通过预检，固定划分规模如下：

| 数据集 | train 图像 | val 图像 | test 图像 |
|---|---:|---:|---:|
| 8-calves | 700 | 200 | - |
| animals_10 | 1,293 | 323 | - |
| CBPD_ODD | 292 | 73 | - |
| CID | 1,645 | 411 | - |
| CImage | 141 | 35 | - |
| COCO | 1,376 | 344 | - |
| COLO | 803 | 201 | - |
| Cows2021 | 7,248 | 1,023 | 2,131 |
| diarycow | 3,140 | 560 | 420 |
| Google Open Image Dataset | 2,333 | 583 | - |
| HCRD | 851 | 212 | - |
| MooTrack360 | 1,200 | 300 | - |
| NWAFU_CD | 1,503 | 375 | - |
| XGain | 1,326 | 331 | - |
| **合计** | **23,851** | **4,971** | **2,551** |

`COCO`、`NWAFU_CD` 和 `CImage` 的有效运行目录分别使用
`COCO_new1class`、`NWAFU_CD_new1class` 和 `CImage_new1class`，这是合并为单类别后的版本。

### 2.3 统一训练配置

| 项目 | YOLO11s/YOLO11l 配置 |
|---|---|
| 初始化权重 | `models/yolo11s.pt` 或 `models/yolo11l.pt` |
| 训练轮数 | 100 epochs |
| batch size |  16|
| 输入尺寸 | `640 x 640` |
| GPU | `device=0` |
| DataLoader workers | 8 |
| AMP | 开启，`amp=True` |
| 随机种子 | 42 |
| 确定性 | `deterministic=True` |
| 预训练 | 开启，`pretrained=True` |
| 训练任务 | detect，单类别 `cow` |

14 个数据集按固定顺序串行训练，避免多个任务同时占用 GPU。每个数据集训练时先执行
数据预检，再调用对应的 YOLO 训练入口。训练完成后均生成：

```text
outputs/yolo11s/<run>/results.csv
outputs/yolo11s/<run>/weights/best.pt
outputs/yolo11s/<run>/weights/last.pt

outputs/yolo11l/<run>/results.csv
outputs/yolo11l/<run>/weights/best.pt
outputs/yolo11l/<run>/weights/last.pt
```

如果训练中断，批量脚本会保留当前日志，并可从 `last.pt` 继续；已经完成 100 epochs 且存在
`best.pt` 的 run 会被跳过。两套模型的 14 个正式 run 均完成 100 epochs。

### 2.4 实际执行入口

进入远程项目并激活 Ultralytics 环境：

```bash
source /data1/yxli/miniconda3/etc/profile.d/conda.sh
conda activate ultralytics
cd /data1/yxli/CODE/ultralytics/self_mAP
```

预检、单数据集训练和 14 集串行队列命令如下：

```bash
python scripts/check_yolo11s.py --json logs/yolo11s_14/preflight.json
python scripts/check_yolo11l.py --json logs/yolo11l_14/preflight.json

python scripts/train_yolo11s.py Cows2021 --epochs 100 --batch 32 --imgsz 640 --device 0
python scripts/train_yolo11l.py Cows2021 --epochs 100 --batch 32 --imgsz 640 --device 0

bash scripts/run_yolo11s_all.sh --dry-run
bash scripts/run_yolo11l_all.sh --dry-run
```

正式批量队列可以放在断开安全的后台会话中运行，例如：

```bash
tmux new-session -d -s yolo11s_all 'bash scripts/run_yolo11s_all.sh'
tmux new-session -d -s yolo11l_all 'bash scripts/run_yolo11l_all.sh'
```

队列日志分别写入 `logs/yolo11s_14/queue.log` 和 `logs/yolo11l_14/queue.log`；本次完成后的
评估执行记录为 `logs/yolo11_eval.status`。

## 3. 测试与评估流程

### 3.1 评估脚本

评估脚本加载每个训练 run 的 `weights/best.pt`，调用 Ultralytics `model.val()`，使用对应
数据集 YAML 和既有 split：

```bash
python scripts/evaluate_yolo11s.py --all \
  --imgsz 640 --batch 32 --device 0 --workers 8
python scripts/summarize_yolo11s.py

python scripts/evaluate_yolo11l.py --all \
  --imgsz 640 --batch 32 --device 0 --workers 8
python scripts/summarize_yolo11l.py
```

`--all` 参数曾因 Python 3.10 中 `argparse` 对 `nargs="*" + choices` 的处理而收到空列表
并报错。已将两个评估脚本改为解析后显式校验数据集名称，修复后重新执行成功。

### 3.2 评估指标与输出

每个数据集记录以下检测指标：

- `Precision`
- `Recall`
- `mAP50`：IoU=0.50
- `mAP50-95`：IoU 0.50--0.95 的平均精度

评估结果和可视化保存在：

```text
/data1/yxli/CODE/ultralytics/self_mAP/outputs/evaluations/yolo11s/<run>_<split>/
/data1/yxli/CODE/ultralytics/self_mAP/outputs/evaluations/yolo11l/<run>_<split>/
```

每个目录下的 `metrics.json` 保存评估参数、实际 split、checkpoint 和指标。
两套模型的串行评估均在远程 `tmux` 会话 `yolo11_eval` 中执行，连接断开不会终止任务。

## 4. YOLO11s 正式评估结果

下表的“峰值 epoch”是训练 `results.csv` 中 `metrics/mAP50-95(B)` 最高的 epoch；评估指标
是使用该 run 的 `weights/best.pt` 在指定 split 上重新计算的结果。Ultralytics 的 `best.pt`
按综合 fitness 保存，因此峰值 epoch 与 checkpoint 对应 epoch 在个别 run 中可能不同。

| 数据集 | split | 峰值 epoch | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---:|---:|---:|---:|---:|
| 8-calves | val | 53 | 0.9520 | 0.9412 | 0.9666 | **0.5530** |
| animals_10 | val | 92 | 0.8762 | 0.7945 | 0.8717 | **0.6808** |
| CBPD_ODD | val | 79 | 0.9892 | 0.9955 | 0.9948 | **0.9500** |
| CID | val | 97 | 0.9507 | 0.9502 | 0.9861 | **0.8764** |
| CImage | val | 1 | 0.9138 | 0.8839 | 0.9345 | **0.7766** |
| COCO | val | 77 | 0.8315 | 0.6816 | 0.7805 | **0.5161** |
| COLO | val | 78 | 0.9102 | 0.8886 | 0.9491 | **0.6536** |
| Cows2021 | test | 55 | 0.9619 | 0.9854 | 0.9831 | **0.8771** |
| diarycow | test | 87 | 0.9962 | 0.9847 | 0.9945 | **0.8797** |
| Google Open Image Dataset | val | 87 | 0.8267 | 0.6626 | 0.7296 | **0.4541** |
| HCRD | val | 89 | 0.9922 | 0.9724 | 0.9930 | **0.9373** |
| MooTrack360 | val | 96 | 0.9439 | 0.8957 | 0.9612 | **0.6562** |
| NWAFU_CD | val | 100 | 0.8706 | 0.8371 | 0.9113 | **0.7332** |
| XGain | val | 99 | 0.9815 | 0.9820 | 0.9943 | **0.8249** |

## 5. YOLO11l 正式评估结果

| 数据集 | split | 峰值 epoch | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---:|---:|---:|---:|---:|
| 8-calves | val | 68 | 0.9502 | 0.9472 | 0.9711 | **0.5624** |
| animals_10 | val | 89 | 0.8938 | 0.7795 | 0.8714 | **0.6853** |
| CBPD_ODD | val | 89 | 0.9759 | 0.9891 | 0.9927 | **0.9395** |
| CID | val | 57 | 0.9415 | 0.9486 | 0.9855 | **0.8743** |
| CImage | val | 1 | 0.8630 | 0.9667 | 0.9463 | **0.7998** |
| COCO | val | 90 | 0.8212 | 0.7067 | 0.7769 | **0.5212** |
| COLO | val | 80 | 0.9185 | 0.8976 | 0.9557 | **0.6532** |
| Cows2021 | test | 42 | 0.9586 | 0.9867 | 0.9821 | **0.8715** |
| diarycow | test | 99 | 0.9896 | 0.9889 | 0.9930 | **0.8838** |
| Google Open Image Dataset | val | 76 | 0.7974 | 0.6825 | 0.7337 | **0.4611** |
| HCRD | val | 98 | 0.9840 | 0.9755 | 0.9922 | **0.9343** |
| MooTrack360 | val | 100 | 0.9510 | 0.9205 | 0.9693 | **0.6758** |
| NWAFU_CD | val | 98 | 0.8647 | 0.8553 | 0.9161 | **0.7394** |
| XGain | val | 99 | 0.9886 | 0.9655 | 0.9838 | **0.8257** |

## 6. 宏平均与模型对比

以下为 14 个数据集等权宏平均，不按图片数量或标注框数量加权：

| 指标 | YOLO11s | YOLO11l |
|---|---:|---:|
| mAP50 宏平均 | 0.9322 | 0.9336 |
| mAP50-95 宏平均 | 0.7406 | 0.7448 |
| YOLO11l 更高的数据集数量 | - | 9/14 |

YOLO11l 的 mAP50-95 宏平均比 YOLO11s 高约 `0.0042`，但不是所有数据集都更高：
YOLO11l 在 `CImage` 和 `MooTrack360` 上提升较明显，在 `CBPD_ODD`、`Cows2021` 和 `HCRD`
上低于 YOLO11s。该宏平均仅用于描述这次固定协议下的结果，不能据此推断跨数据集泛化能力。

## 7. 结果与 checkpoint 位置

YOLO11s 汇总文件：

```text
/data1/yxli/CODE/ultralytics/self_mAP/logs/yolo11s_14/summary.csv
/data1/yxli/CODE/ultralytics/self_mAP/logs/yolo11s_14/summary.json
```

YOLO11l 汇总文件：

```text
/data1/yxli/CODE/ultralytics/self_mAP/logs/yolo11l_14/summary.csv
/data1/yxli/CODE/ultralytics/self_mAP/logs/yolo11l_14/summary.json
```

训练日志和状态文件分别位于：

```text
/data1/yxli/CODE/ultralytics/self_mAP/logs/yolo11s_14/
/data1/yxli/CODE/ultralytics/self_mAP/logs/yolo11l_14/
/data1/yxli/CODE/ultralytics/self_mAP/logs/yolo11_eval.status
```

每个数据集的最佳权重路径格式为：

```text
/data1/yxli/CODE/ultralytics/self_mAP/outputs/yolo11s/<run>/weights/best.pt
/data1/yxli/CODE/ultralytics/self_mAP/outputs/yolo11l/<run>/weights/best.pt
```

例如，`CImage` 的有效运行目录为 `CImage_new1class`，`COCO` 的有效运行目录为
`COCO_new1class`，`NWAFU_CD` 的有效运行目录为 `NWAFU_CD_new1class`。

## 8. 结果分析与限制

1. `CBPD_ODD` 是 YOLO11s 本次评估的最高数据集，mAP50-95 为 `0.9500`；YOLO11l 在该数据集为
   `0.9395`。`Google Open Image Dataset` 和 `COCO` 的 mAP50-95 相对较低，分别约为
   `0.454--0.461` 和 `0.516--0.521`。
2. `CImage` 只有 176 张图像，两个模型的训练峰值都在第 1 epoch，存在明显的小样本和快速
   过拟合风险，实际部署应使用 `best.pt` 并结合更多数据复核。
3. `Cows2021` 和 `diarycow` 使用已有 `test` 视图；由于既有划分审计发现 `diarycow` 存在
   train/test 18 张、train/val 4 张及 val/test 5 张重复图像，这些 test 指标不能解释为
   完全无泄漏的独立泛化结果。
4. 历史审计还发现 `NWAFU_CD` 的 train/val 有 5 张重复图像、`XGain` 的 train/val 有 3 张
   重复图像。其余数据集的结果同样应理解为“沿用既有划分”的基线结果。
5. 不同数据集的来源、目标尺度、场景复杂度和标注密度差异较大，mAP 只适合在相同数据版本、
   类别定义、输入尺寸和评估协议下比较，不能直接作为绝对模型排名。

## 9. 结论

在统一单类别 `cow`、固定数据集划分、`640 x 640` 输入和 100 epochs 的协议下，YOLO11s 和
YOLO11l 均完成了 14 个数据集的训练与评估。正式结果已经分别保存到 `summary.csv/json` 和
各数据集的 `metrics.json`，训练 checkpoint 同时保留 `best.pt` 与 `last.pt`。在本次同域协议
下，YOLO11l 的 mAP50-95 宏平均略高于 YOLO11s，但两者差异应结合逐数据集结果和上述划分限制
解读；后续跨域研究应固定最佳 checkpoint，建立 14 x 14 的交叉评估矩阵，并先处理已发现的
跨划分重复图像。
