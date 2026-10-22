---
id: cowcv-indomain-architecture-evidence
type: source
status: draft
created: 2026-10-13
updated: 2026-10-14
sources:
  - 牛只数据集/域内模型与架构比较.md
  - 牛只数据集/文章初稿.md
  - 科研记录/实验记录格式参考.md
  - 牛只数据集/10月域内重测计划.md
  - 牛只数据集/域内重测-10月.md
  - 牛只数据集/9月LODO泛化测试计划.md
  - 牛只数据集/LODO测试-9月.md
  - https://docs.ultralytics.com/models/yolo11/
  - https://arxiv.org/abs/2304.08069
  - https://arxiv.org/abs/1506.01497
  - https://arxiv.org/abs/1708.02002
  - https://mmdetection.readthedocs.io/en/v3.3.0/advanced_guides/customize_dataset.html
  - https://mmengine.readthedocs.io/en/latest/api/generated/mmengine.optim.OptimWrapper.html
  - https://mmengine.readthedocs.io/en/latest/api/generated/mmengine.hooks.CheckpointHook.html
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/utils/metrics.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/models/rtdetr/predict.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/models/rtdetr/val.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/engine/trainer.py
  - https://arxiv.org/abs/1612.03144
  - https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py
  - https://docs.ultralytics.com/modes/val/
  - https://arxiv.org/html/2007.01434v1
  - https://github.com/pytorch/pytorch/blob/v2.5.1/docs/source/data.rst
  - https://github.com/pytorch/pytorch/blob/v2.5.1/docs/source/notes/randomness.rst
---

# 牛只域内模型与架构比较：历史验证记录及方法核查

## 资料范围与定位

主要来源为 [服务器核查记录](../../牛只数据集/域内模型与架构比较.md)与 [文章初稿](../../牛只数据集/文章初稿.md)的 §3.2、§4.1–4.3、附表 A1。训练时段为 2026-07-11 至 08-06，核查笔记含 09-02、09-06 与后续补记。本页于 2026-10-13 整理，关联成文 [科研记录：多源留一域泛化](../../科研记录/多源留一域泛化.md)。

2026-10-14补充完整读取用户指定的[9月LODO计划](../../牛只数据集/9月LODO泛化测试计划.md)与[LODO执行记录](../../牛只数据集/LODO测试-9月.md)，并核对新域内test主表和es相关段落。新增内容集中于科研记录§7.4，以域内参照衔接固定YOLO11m的多源泛化。

本次只读取本地文档和外部官方资料，没有重开历史远程日志、checkpoint、逐图预测或 56 份 metrics.json。历史执行事实为本地记录转述；本地表格复算不伪装为远程原始输出。

## 来源明确记载的内容

- 四种检测器为 YOLO11m、RT-DETR-L、Faster R-CNN R50-FPN、RetinaNet R50-FPN；每种在 14 个数据集内分别训练，共 56 个组合，历史主表全部为 val。
- 名义轮数均为 100，但输入、AMP、实际优化器、micro-batch、累积与环境不同。记录中的稳态有效 batch 为 64／60／16／16，不等于实际更新次数。
- 本地排障记录涉及矩形输入、重复预测匹配顺序和插值曲线与严格阈值计数；主工作点为 conf=0.25、匹配 IoU≥0.5，最佳 F1 阈值在 val 上选取。
- [10月重测计划](../../牛只数据集/10月域内重测计划.md)与 [执行记录](../../牛只数据集/域内重测-10月.md)限定新一轮为 YOLO11m×14；四架构统一复核另行排期。新 test 值不混入旧四模型 val 表。
- 9月LODO记录固定YOLO11m、13源每源每轮500图、batch=nbs=16、100 epochs、AdamW@0.002、源val等权宏平均选模、并列较早；seed=42/43/44完成14fold重复，all14仅主方案。
- 新数据规模为25079/3142/3124，共31345图；旧架构规模为23851/4971/2551，共31373图，划分同时变化，两个阶段均值不可直接相减解释退化。

## 复算与综合判断

从初稿逐域表复算，AP50–95 宏平均依次为 0.7390、0.7437、0.7022、0.7001。RT-DETR-L 与 YOLO11m 的平均差为 0.0047，领先域数为 9／5，12/14 域绝对差不超过 0.02。

四模型两两 Spearman 相关为 0.9736–0.9912；数据集四模型均值跨度为 0.4949，模型宏平均跨度为 0.0435。它们支持共同相对次序与协议内描述，不构成普遍架构排名、数据集质量排名、因果归因或统计显著性。

8-calves、MooTrack360、COLO 的 AP50 较高而 AP50–95 下降较大，提示进一步审核定位与标注；COCO、Google 牛类子集在 AP50 下也存在困难。固定与最佳工作点 F1 的差异只说明阈值敏感性，不证明分数形态或独立 test 收益。

完整表格与派生统计见 [可编辑底稿](../../科研记录/多源留一域泛化.assets/表格可编辑底稿.md)、[56 组合 CSV](../../科研记录/多源留一域泛化.assets/逐模型逐数据集指标.csv)与 [复算 JSON](../../科研记录/多源留一域泛化.assets/数值复算.json)。

## LODO与新域内参照的补充复算

从LODO三轮四位逐域AP表复算，三轮宏平均约0.5056/0.5009/0.5034，均值0.5033，总体SD约0.0019（ddof=0）；若用样本SD约0.0024。三轮排序Spearman为1.0000/0.9912/0.9912。42个结果的14目标视图合计3124图。

与新域内stock seed42逐域配对，监督AP宏平均0.7214，逐域保持率宏平均0.7328；两个AP宏平均相除约0.6976，不等于保持率宏平均。CImage的保持率约1.4865、MooTrack360约0.2080；经验监督参照不是理论上限，不裁剪R>1。

新域内es扩展0.7205±0.0016使用样本SD，stock重复仅反映运行间稳定性；不混入上述分母。匹配新data/test的单源14×14增益、外部E及预算匹配对照尚需执行。现有结果不能证明四架构跨域排名或域多样性的净因果收益。

全部复算及舍入差异见[本次JSON](../../科研记录/多源留一域泛化.assets/LODO与域内复算-20261014.json)、[三种子与域内参照CSV](../../科研记录/多源留一域泛化.assets/LODO三种子与域内参照-20261014.csv)和[新增表格底稿](../../科研记录/多源留一域泛化.assets/LODO补充表格可编辑底稿-20261014.md)。

## 官方方法核查与冲突

外部原理依据来自 YOLO11 官方文档及 RT-DETR、Faster R-CNN、Focal Loss、FPN 原始论文。单类别配置、梯度累积与保存机制对应 MMDetection／MMEngine 官方指南；匹配扫描和 maxDets 对应 COCO API。具体引用定位见科研记录附录 A。

需保留的冲突为：

1. 初稿有效 batch 总括句与 RT-DETR 的 12×5=60 不一致。
2. 核查笔记硬件节“全部 28 run”与四模型×14 的 56 组合不一致；28 只可明确用于两种 Ultralytics 模型的组合数。
3. 输入设置矩形面积比为 2.6035，不能沿用“约 4 倍”，更不能当计算成本比。
4. 官方 `v8.4.92` 的检测 fitness 权重为 `[0,0,0,1]`，与笔记的 0.1／0.9 公式冲突；需查历史安装源码／补丁。
5. 初稿附录说明 P/R/F1 使用 best.pt，并有 3 个 Ultralytics run 与 mAP 最高轮不同；不能将所有指标称为同轮结果。
6. RT-DETR 官方 predictor 使用 scale-fill 与专用后处理，不能套用统一 letterbox／NMS 描述；历史自定义评测仍待查。
7. LODO默认val汇总P/R未证明为固定conf=0.25的严格计数。官方版本指标代码取平滑F1峰值，需确认历史脚本是否另算工作点，不能并入四架构固定阈值表。
8. LODO为407步／轮、末批4张；all14为438步、末批8张。晚期峰值不能单独证明收敛；目标路径隔离与精确去重也不能证明采集来源独立或排除预训练重叠。
9. LODO记录与新域内记录的部分SD字段冲突；本页使用三轮AP直接复算，不猜测另一聚合字段语义。旧test_instances误记含目标图数的事件按新域内§3.2说明保留。

## 待核实与后续入口

历史远程产物的当前存在性、代码身份、逐权重 hash、全部实际输入张量与后处理、匹配全覆盖、更新次数和完整计算成本均未核查。正式四架构复核需同数据版本与冻结 test、明确预算与选模规则、统一 evaluator，并分别报告训练随机性与测试样本不确定性。

参见 [数据集整理与独立测试评估的来源核查](cowcv-dataset-test-evaluation-evidence.md)，理解历史划分与独立性边界；两页分别承担数据准备与架构比较的来源定位。
