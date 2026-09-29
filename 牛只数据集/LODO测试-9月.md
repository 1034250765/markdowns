# LODO 测试：过程与结果

> 执行时间：2026-09-24 至 2026-09-28
> 实验设计：见 `9月LODO泛化测试计划.md`（第 3.2 节训练协议）
> 训练与推理服务器：实验室服务器 `yxli@211.69.141.71`，项目根 `/data1/yxli/LODOANDClassbyDomain`
> 硬件：NVIDIA A100-PCIE-40GB（单卡），Ultralytics 8.4.92 + PyTorch（CUDA）

---

## 一、实验概述

本实验执行《9月LODO泛化测试计划》的**多源 LODO 主实验**（计划优先级 2）：每次完整留出一个数据集作为目标域，用其余 13 个数据集按固定配额联合训练 YOLO11m，在目标域 **test 冻结视图**上做零样本推理，得到有向迁移结果 $M_{-t \rightarrow t}$。另训练一个**全 14 源模型（all14）**，供后续外部数据集 E 零样本测试（计划优先级 1）使用。

核心协议要点（全部预先冻结，未看结果后调整）：

- 检测器 YOLO11m、单类别 `cow`、imgsz=640、100 epochs、AMP；
- batch=16、**nbs=16 → accumulate=1**（启动断言 + 每 epoch 步数断言核验）；
- **AdamW、lr0=0.002**，其余超参保持 Ultralytics 默认（与基线一致）；
- **每 epoch 每源抽样配额 q=500**（数据集等权；池 6500 张，all14 为 7000 张）；
- 源训练集 < 500 者（CImage=141、CBPD_ODD=292）有放回抽样，重复率记录于 `sample_stats.csv`；
- **末 batch 不足 16 张时保留**（6500 = 406 满批 + 1 个 4 张批 = 每 epoch 407 步）；
- 每 epoch 在全部 13 个源域 val 上分别验证，记录每域 mAP 并计算**等权宏平均**；
- checkpoint 保存每 epoch 一个；选择规则 = **源域宏平均最高 epoch，并列取较早**（计划 3.2.4）；
- 主随机种子 seed=42（训练层）+ 抽样清单种子 42（抽样层），单种子串行执行；
- 目标域 train/val/test 在训练、调参、checkpoint 选择阶段零接触，仅在最终评测出现一次。

---

## 二、数据与目录基础（2026-09-23/24 准备）

### 2.1 数据基础

- 14 个数据集，Ultralytics 标准结构，**权威数据源为 `data/` 目录**（SHA-256 同图同标去重后，总计 train 25,079 / val 3,142 / test 3,124 = 31,345）。
- `splits/*.txt` 清单与磁盘逐名复核一致（三个受去重影响的数据集于 09-24 重建清单，旧清单备份于 `splits/_historical/_pre_dedup_cleanup_20260924/`）。

### 2.2 LODO 目录体系（`lodo/`）

```text
lodo/
├── protocol.yaml            # 冻结协议（所有 fold 一致）
├── labels_db_train.pkl      # 全量 train 标签库（一次性构建，15 fold 复用）
├── folds/<fold>/            # 15 个：lodo_<目标数据集> ×14 + all14
│   ├── fold.yaml            # fold 元信息（target/sources/q/seed/val 视图）
│   ├── sample_lists/        # 预生成抽样清单 epoch_001..100.txt（每源 500 行/块）
│   ├── sample_stats.csv     # 每 epoch×数据集 重复率统计
│   ├── logs/train/          # metrics.csv（每 epoch 完整记录）+ run_info.json
│   └── runs/train/          # weights/epoch{N}.pt + last/best + selected.pt 等
├── logs/driver.log          # 串行训练驱动器日志
└── results/                 # 目标域零样本评测结果
```

### 2.3 抽样与随机性规则

- **抽样层**：每 epoch 每源 q=500 张，RNG 种子 `LODO|main=<seed>|epoch=<e>|ds=<名>`（Python 字符串 seed 走 sha512，跨平台确定）。同一 (epoch, 数据集) 的样本在所有含该源的 fold 中完全一致，跨 fold 数据组成可精确对齐。清单**预生成并冻结**（可 md5 审计），训练时不再重抽。
- **训练层**：数据增强与洗牌由 seed=42 驱动（洗牌种子 = seed × 1048576 + epoch，逐 epoch 不同且确定）。
- **初始化层**：全部 fold 从同一份 `yolo11m.pt` 初始化。
- 多种子重复机制已就绪（`make_lodo_dirs.py --seed S` 生成 `sample_lists_seed<S>/`，训练时 `--seed S --sampling-seed S`），本次按决定**暂不使用**；只改训练 seed 而清单不变属于"训练随机性重复"，不构成完整多种子重复。

---

## 三、执行过程

### 3.1 工程实现要点

训练脚本 `lodo_train.py`（基于 Ultralytics `DetectionTrainer` 子类化）的四个关键实现决策：

1. **每 epoch 重建 DataLoader**：Ultralytics 持久 worker 进程在 fork 后看不到主进程对数据集对象的修改，若只在主进程换清单，worker 会静默使用第 1 个 epoch 的清单。改为每 epoch 新建数据集+loader，彻底规避。
2. **标签库替代 stock 的 .cache**：每 epoch 清单不同、hash 必不匹配，走 stock 逻辑会反复重扫并覆盖源数据集自身的 `labels/train.cache`。改为一次性预建全量标签库（`labels_db_train.pkl`，25,079 张，stock 校验逻辑）。
3. **洗牌种子显式化**：stock 的固定 generator 种子在逐 epoch 重建 loader 时会导致每个 epoch 顺序相同，改为 `seed × 1048576 + epoch`。
4. **stock best.pt 不作为选择依据**：stock 在宏平均并列时保留较晚 epoch，与计划"并列取较早"相反；正式选择一律以 `logs/train/metrics.csv` + `select_checkpoint.py` 为准（输出 `selection.json` 存档依据）。

其余保证：`close_mosaic=10`（Ultralytics 默认）在逐 epoch 重建数据集下正确复刻；stock 的单数据集 final_eval 跳过（只做 last/best 优化器剥离）；加载清单时断言每源恰 500 张、目标域路径零出现。

### 3.2 时间线

| 时间 | 事件 |
|---|---|
| 09-24 | 生成 15 fold 目录与 1500 份抽样清单（md5 幂等验证）；重建 3 个数据集的 stale 清单 |
| 09-26 01:06 | 启动 `lodo_Cows2021`；随后串行驱动器 `run_all_folds.sh` 挂起等待（flock 防双开） |
| 09-26 04:02 → 09-27 20:43 | 串行接力剩余 14 个 fold，**15/15 全部完成，退出码全 0** |
| 09-27 晚 | 15 个 fold 逐一执行 checkpoint 选择；目标域零样本评测（28 次推理） |

总训练耗时约 **43.6 小时**（每 fold 约 2 小时 56 分，每 epoch 约 108 s，其中训练约 85 s、13 源验证约 20 s）。

### 3.3 过程中捕获并修复的问题

| 问题 | 修复 |
|---|---|
| `data/` 下隐藏的 `.ipynb_checkpoints` 目录被标签库构建误当数据集 | 改为跳过隐藏目录 + 必须含 `images/train` + 断言恰好 14 个 |
| `copy(self.args)` 误将 copy 模块当函数 | 改 `copy.copy(...)` |
| rect 验证的数据集分组 batch 与 loader batch 不一致（16 vs 32）导致 collate 崩溃 | 两者统一为 batch×2 |
| 抽样清单生成时发现 `splits/` 旧清单残留 28 个已去重删除的文件名 | 以 `data/` 为权威重建三个数据集清单（旧清单备份） |

### 3.4 质量核验（全程生效的断言）

- 每 epoch 实际 `optimizer.step()` 次数 == ⌈池/16⌉（407/438），**末 batch 的 4 张图从未被丢弃**；
- `accumulate == 1` 启动断言；
- 每 epoch 加载清单时：行数 == 训练池、每源恰 500 张、目标域路径零出现（零泄漏）；
- 每 epoch 记录清单 md5、采样数/唯一数（重复数与 `sample_stats.csv` 理论值一致，如 6500 中唯一 5882 ≈ 理论 618 重复）；
- 清单生成脚本幂等：重跑 30 份抽样清单 md5 逐字节一致。

---

## 四、结果

### 4.1 Checkpoint 选择（`select_checkpoint.py`，宏平均最高、并列取较早）

| Fold | e* | 源域宏平均 mAP50-95 | | Fold | e* | 源域宏平均 |
|---|---:|---:|---|---|---:|---:|
| lodo_8-calves | 100 | 0.760 | | lodo_Cows2021 | 98 | 0.740 |
| lodo_animals_10 | 99 | 0.752 | | lodo_diarycow | 100 | 0.742 |
| lodo_CBPD_ODD | 100 | 0.733 | | lodo_Google_Open_Images | 100 | 0.772 |
| lodo_CID | 100 | 0.739 | | lodo_HCRD | 94 | 0.736 |
| lodo_CImage | 98 | 0.737 | | lodo_MooTrack360 | 97 | 0.753 |
| lodo_COCO | 100 | 0.765 | | lodo_NWAFU_CD | 97 | 0.756 |
| lodo_COLO | 99 | 0.756 | | lodo_XGain | 100 | 0.747 |
| all14 | 99 | 0.751 | | | | |

所有 fold 均无并列（并列 1 个）；e* 集中在 epoch 94–100，说明 100 epoch 预算基本充分、训练接近收敛。

### 4.2 目标域零样本结果 `M_{-t→t}`（selected.pt，test 冻结视图，imgsz=640）

| 目标域 | test 图数 | mAP@0.5 | mAP@0.5:0.95 | P | R |
|---|---:|---:|---:|---:|---:|
| CBPD_ODD | 36 | 0.974 | **0.919** | 0.970 | 0.958 |
| CID | 205 | 0.876 | 0.742 | 0.885 | 0.793 |
| CImage | 17 | 0.905 | 0.692 | 0.815 | 0.970 |
| animals_10 | 161 | 0.845 | 0.658 | 0.852 | 0.781 |
| diarycow | 408 | 0.945 | 0.623 | 0.940 | 0.884 |
| XGain | 163 | 0.810 | 0.561 | 0.895 | 0.775 |
| NWAFU_CD | 185 | 0.670 | 0.509 | 0.869 | 0.566 |
| COCO | 172 | 0.721 | 0.495 | 0.777 | 0.650 |
| Google_Open_Images | 291 | 0.712 | 0.429 | 0.786 | 0.663 |
| COLO | 100 | 0.665 | 0.391 | 0.803 | 0.567 |
| 8-calves | 90 | 0.766 | 0.353 | 0.806 | 0.722 |
| HCRD | 106 | 0.574 | 0.290 | 0.635 | 0.583 |
| Cows2021 | 1040 | 0.733 | 0.275 | 0.628 | 0.845 |
| MooTrack360 | 150 | 0.306 | **0.141** | 0.622 | 0.241 |

**数据集等权汇总**：

| 指标 | 宏平均 | 中位数 | IQR | 最好 | 最差 |
|---|---:|---:|---|---:|---:|
| mAP@0.5:0.95 | **0.506** | 0.502 | [0.337, 0.666] | 0.919 (CBPD_ODD) | 0.141 (MooTrack360) |
| mAP@0.5 | **0.750** | 0.750 | — | 0.974 (CBPD_ODD) | 0.306 (MooTrack360) |

### 4.3 敏感性对照（3.2.4：第 100 epoch 固定预算对照）

`selected.pt` 与第 100 epoch checkpoint 在 14 个目标域上的 mAP@0.5:0.95 **平均绝对差 0.0004、最大差 0.0018**——checkpoint 选择规则对结果不敏感，两条规则给出一致的结论。

### 4.4 初步观察（描述性，不作因果解释）

- **跨域落差很大**：最好与最差目标域相差约 6.5 倍（mAP50-95）。MooTrack360（顶视全景追踪域）是迁移最难的目标域；其低召回（0.24）说明检测头难以迁移到该域的目标外观。
- **"找得到、框不准"的分化**：diarycow、Cows2021 等域 mAP@0.5 很高（0.94/0.73）而 mAP@0.5:0.95 偏低（0.62/0.28），说明跨域退化更多体现在**定位精度**而非**检出能力**——Cows2021 高召回（0.85）配合低精确率（0.63）亦符合此模式。
- **与计划解释边界一致**：以上均为**跨数据集有向迁移**结果，各目标域同时改变牛群、相机、视角、光照等混杂因素，不能归因于任何单一环境因素；按域维度分层（计划第三章）是下一步解释性分析的方向。
- CImage（17 张测试图）与 CBPD_ODD（36 张）样本量小，指标方差大，跨域比较时需注明（计划数据质量备注）。

---

## 五、资产位置与可复现性

| 资产 | 路径（服务器 `/data1/yxli/LODOANDClassbyDomain/` 下） |
|---|---|
| 冻结协议 | `lodo/protocol.yaml`；各 fold 元信息 `lodo/folds/<fold>/fold.yaml` |
| 抽样清单 | `lodo/folds/<fold>/sample_lists/`（md5 可审计；生成脚本 `make_lodo_dirs.py`） |
| 训练脚本 | `lodo_train.py`（单 fold）；驱动器 `run_all_folds.sh`（串行） |
| 训练日志 | `lodo/folds/<fold>/logs/train/metrics.csv` + `run_info.json` |
| Checkpoint | `runs/train/weights/epoch{0..99}.pt`（已剥离优化器）、`selected.pt`、`epoch100_final.pt` |
| 选择存档 | `runs/train/selection.json`（`select_checkpoint.py` 产出） |
| 评测脚本 | `lodo_eval_target.py` |
| 评测结果 | `lodo/results/lodo_target_test_results.{csv,json}` |
| 驱动器日志 | `lodo/logs/driver.log` |

复现单次训练/评测：

```bash
conda activate ultralytics && cd /data1/yxli/LODOANDClassbyDomain
python3 lodo_train.py --fold lodo_Cows2021 --device 0      # 默认 seed=42/42
python3 select_checkpoint.py --fold lodo_Cows2021
python3 lodo_eval_target.py
```

环境记录：各 fold `logs/train/run_info.json` 存有 ultralytics/torch/CUDA 版本、GPU 型号、种子规则与协议快照。

---

## 六、结论边界与后续

本实验支持的结论（计划第九节口径）：

> 在固定 YOLO11m 与统一训练/评估协议下，13 个已知牛只视觉数据域等权联合训练后，模型在未参与训练的目标数据集上取得了宏平均 mAP@0.5:0.95 ≈ 0.51（mAP@0.5 ≈ 0.75）的零样本表现；各目标域间差异显著（0.14–0.92），其中对顶视追踪域（MooTrack360）的迁移能力最弱。

**不支持的结论**：环境因素因果归因、普遍适用于所有未知牧场、任何数据集的绝对质量排名。

**后续工作**：
1. 与单源 14×14 基线对比：计算各目标域的保持率 $R^{LODO}_{target}$ 与相对单源均值的增益 $\Delta_{multi}(t)$；
2. 外部数据集 E 零样本测试（计划优先级 1）：使用 `all14` fold 的 `selected.pt`（源域宏平均 0.751，epoch 99）；
3. 按域维度（视角、光照、尺度、密度、遮挡）的事后分层分析（计划第三章）；
4. 多随机种子重复（机制已就绪，按当前决定暂缓）。
