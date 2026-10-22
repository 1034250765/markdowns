---
id: cowcv-dataset-test-evaluation-evidence
type: source
status: draft
created: 2026-10-13
updated: 2026-10-13
sources:
  - 牛只数据集/7月工作.md
  - 牛只数据集/拍摄环境与场景.md
  - 牛只数据集/_remote_matrix/Cows2021.json
  - 牛只数据集/_remote_target_unify/README.md
  - 牛只数据集/域内重测-10月.md
  - 牛只数据集/测试方法.md
  - 科研记录/实验记录格式参考.md
  - https://docs.ultralytics.com/datasets/detect/
  - https://docs.ultralytics.com/modes/val/
  - https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
  - https://github.com/JohannesBuchner/imagehash
  - https://doi.org/10.1016/j.patter.2023.100804
  - https://arxiv.org/abs/2207.07048
  - https://arxiv.org/abs/2105.01938
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/utils/metrics.py
  - https://arxiv.org/abs/2407.20372
  - https://data.bris.ac.uk/data/dataset/4vnrca7qw1642qlwxjadp87h7
---

# 牛只数据集整理与独立测试评估：7月记录及方法核查

## 资料范围与用途

本页整理 2026-10-13 阅读的本地历史记录、已归档评估 JSON、官方操作文档和原始研究。完整实验记录、图表及来源编号见[数据集整理与独立测试集评估](../../科研记录/数据集整理与独立测试集评估.md)，具体来源定位见其附录 A。

主实验时段为 2026-07；后续目标视图修订与 2026-10 重测分别记录，不回填为 7 月完成事项。本次未连接服务器、未重跑训练或评估；网页用于核查方法与接口，不证明历史实例采用相同实现。

## 来源事实

- [7月工作](../../牛只数据集/7月工作.md)§1、§8、§12 记载，两模型各有 14 个有效单类别单数据集结果。首批 YOLO11m batch=16，后续 32；RT-DETR-L batch=12、FP32。相同 epoch 数不能单独建立预算可比性。
- 月报 §3–4 记录 COCO、NWAFU_CD、CImage 的 `Cow/cow` 重复类别修正，旧结果归档，有效结果使用单类别视图。
- 月报 §6 记录 Cows2021 train/val/test 为 7248/1023/2131，test mAP50–95=0.8629；[本地 JSON](../../牛只数据集/_remote_matrix/Cows2021.json)中 `in_domain=true` 的记录支持 `split=test`、2131 张与四位小数指标。两材料记录目录不同，只确认读数一致。
- 月报 §7 记录 Dairy Cow test 420 张、mAP50–95=0.8820；§13.6 后来确认 train→test 精确重复 18 张。该指标保留为有划分污染说明的历史读数，本次未直接打开 Dairy Cow test 原始评估文件。
- 月报 §10 的 AutoDL CID-NOYT 按 514 个牛 ID 分组，评估 103 组/412 张，同时用于验证选择 best；0.8760 是分组自测/验证读数，不能升级为未参与选模的第三个独立 test。
- 月报 §13.6–13.7 记载，31373 个图像逻辑条目有 31254 个唯一 SHA-256；跨数据集精确重复为 0，但人工复核确认 COCO 与 Google 的训练到验证近重复 9 对。pHash 候选数与确认泄漏数应分开。

## 冲突与解释边界

1. **Dairy Cow 的早期“无跨划分重复”与后期审计冲突。** 后期内容级审计更直接，支持限定早期文件检查的结论。train→test 18 张与 val↔test 5 张没有本次成员清单，不能直接相加。
2. **XGain 来源组无重叠与内容重复并存。** 月报 §11 的分组规则未覆盖 §13.6 后来发现的 train→val 3 张精确重复，不能据分组声明否定审计。
3. **Google checkpoint 选择原因待追溯。** 月报 §11.3 将 epoch 74 的 best.pt 与 epoch 89 的最高 mAP50–95 差异归因于综合 fitness；本次核查的官方 v8.4.92 `Metric.fitness()` 只取 mAP50–95。应核对当时安装源码和 checkpoint 元数据，不能静默采用其中一方。
4. **Cows2021 框语义待核对。** [场景档案](../../牛只数据集/拍摄环境与场景.md)记录原始躯干旋转框及水平外接框，月报记录类别筛选与重新标注。原始标签、转换和人工重标的版本关系仍应逐数据集核实。
5. **近重复修订范围的时间差异。** 7 月记录建议先重评两个污染方向；[统一目标视图说明](../../牛只数据集/_remote_target_unify/README.md)后来补齐完整目标列，确保相同目标域的样本集合一致。

## 方法核查与综合判断

Ultralytics 官方文档支持五字段 YOLO 标签、显式 `split="test"` 和指标读取。`model.val(iou=0.7)` 的 IoU 参数是 YOLO NMS 设置，AP 的匹配阈值范围另计；默认汇总 P/R 来自 F1 最优工作点，不改写为固定 conf=0.25 的结果。

GroupShuffleSplit 支持按来源组划分，比例针对组数；时间外推需要另外定义时间隔离。ImageHash 文档支持 pHash 与汉明距离操作，但不为项目 `≤4` 候选阈值提供普遍的同图保证。数据泄漏研究用于解释评估独立性；Cows2021 与 COLO 原始研究用于确认任务与场景背景。

**综合判断：** 7 月形成了可追溯的单类别检测准备与域内基线，但完整、无已知泄漏的 14 数据集独立 test 比较不能由这些记录直接成立。正式报告应同时冻结标签、样本来源、划分、选模规则和评估设置。

**待核实：** 历史远程产物当前存在性、成员级重复清单、标签边界一致性、Dairy Cow 清理后 test 结果及 Google 历史选模实现。2026-10 的后续重测按其本地记录说明，未在本次远程复核。

## 归档说明

科研记录使用 Study Image 方法示意和表格母版；表中数值由程序排入，统计图由固定读数绘制。可编辑表格、数值 JSON、绘图脚本与来源 hash 保存在同名 assets 目录。原始资料未改写；数据库和向量索引同步未运行。
