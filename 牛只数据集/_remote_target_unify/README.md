# TargetUnifyTests — 冻结统一目标视图评测

## 目的

为 14×14 YOLO11m 跨数据集矩阵补齐三个目标列的统一冻结视图，消除
`文章初稿.md` 4.5.1 节记录的评测视图不统一问题（对应投稿审阅意见第3条）。

## 冻结视图

| 目标 | 视图 | 图像数 | 数据位置 |
|---|---|---:|---|
| Cows2021 列 | `test` 划分 | 2,131 | `self_mAP/datasets/Cows2021` |
| Google OI 列 | 近重复清理修订视图 | 576 | `revisions/20260729_.../views/coco_source/data/Google_Open_Images` |
| COCO 列 | 近重复清理修订视图 | 342 | `revisions/20260729_.../views/google_open_image_source/data/COCO` |

COCO 与 Google Open Image cow subset 没有独立 test 划分，两列采用
2026-07-29 感知哈希审计后的修订视图；预训练基线（PretrainedYOLO11mBaseline）
已在用相同视图。

## 评测范围（39 次 + 基线 1 次）

- Cows2021 列（test 2,131）：13 个非 Cows2021 源模型。
  Cows2021 自身对角线已有同视图结果（Cows2021OOD `runs/Cows2021_test`，0.8629），复用不重跑。
- Google OI 列（576）：12 个非 Google 非 COCO 源模型 + Google 模型自身（新域内分母）。
  COCO→Google 已在 20260729 修订中按 576 评测（0.3985），复用不重跑。
- COCO 列（342）：12 个非 COCO 非 Google 源模型 + COCO 模型自身（新域内分母）。
  Google→COCO 已按 342 评测（0.4737），复用不重跑。

另有一次预训练基线评测（`script/evaluate_pretrained_cows2021_test.py`）：原始
`yolo11m.pt` 在 Cows2021 `test` 2,131 张视图上重评，使第4.5.3节 Δ_FT 与矩阵
Cows2021 列同视图。协议复刻 `PretrainedYOLO11mBaseline`：标签机械映射 `0→19`、
保留 COCO 80 类 YAML、仅评估 `classes=[19]`，原图像与标签未修改。结果为
mAP@0.5:0.95 = 0.177726（原 val 1,023 口径为 0.180182），14 域宏平均
0.521021 → 0.520846。

## 评测参数（与既有 14×14 矩阵完全一致）

`imgsz=640`，`batch=12`，`conf=0.001`，`iou=0.7`，`max_det=300`，
`workers=8`，`device=0`，单类别 `cow`，不出图（plots 不影响指标值）。
环境：`miniconda3/envs/ultralytics`（Ultralytics 8.4.92，Python 3.10.18，
torch 2.5.1+cu124）。

## 结果布局

```text
results/yolo11m/
├── runs/<target>/<source>/metrics.json   # 39 个格子，签名含权重、视图、修订清单哈希
├── summary_<target>.json                 # 每列汇总
├── summary.json                          # 全部 39 条记录
└── evaluate.log                          # 运行日志
results/yolo11m_pretrained_cows2021_test/
└── metrics.json                          # 预训练基线在 Cows2021 test 视图的结果
data/pretrained_baseline_Cows2021_test/   # 该基线的临时视图（图像符号链接 + 类别 0→19 标签）
```

metrics.json 已存在且签名一致时自动跳过；签名不一致或残留不完整目录时拒绝
覆盖，需先归档。修订视图的签名记录 `revision_id` 与 `revision_manifest`
SHA-256（`fb40915b3ca2067b625edf336eeedc2905155f114930da620b3dd759ef6bde4f`）。

## 复现

```bash
/data1/yxli/CODE/ultralytics/OOD/TargetUnifyTests/script/run_all.sh
```

## 与既有结果的关系

不修改现有 14 个 `*OOD/` 项目的脚本与结果。矩阵其余 11 列沿用
`*OOD/results/yolo11m/summary.json`；三列取本目录结果，加上三个复用
格子（Cows2021 对角线、COCO→Google、Google→COCO），182 个跨域单元
全部获得同视图目标域分母。
