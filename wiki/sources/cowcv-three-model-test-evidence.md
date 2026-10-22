---
id: cowcv-three-model-test-evidence
type: source
status: draft
created: 2026-10-14
updated: 2026-10-14
sources:
  - 牛只数据集/Retinanet测试.md
  - 牛只数据集/yolo11SL.md
  - 牛只数据集/_效率数据_远程日志提取_20260908.md
  - 牛只数据集/7月工作.md
  - 科研记录/实验记录格式参考.md
  - https://docs.ultralytics.com/models/yolo11/
  - https://docs.ultralytics.com/modes/val/
  - https://docs.ultralytics.com/modes/train/
  - https://mmdetection.readthedocs.io/en/v3.3.0/advanced_guides/customize_dataset.html
  - https://mmdetection.readthedocs.io/en/v3.3.0/user_guides/test.html
  - https://github.com/open-mmlab/mmdetection/blob/v3.3.0/configs/_base_/models/retinanet_r50_fpn.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/utils/metrics.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/engine/trainer.py
  - https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py
  - https://arxiv.org/abs/1708.02002
---

# 牛只三模型测试：RetinaNet与YOLO11s/l历史结果核查

## 范围与来源

本页整理 RetinaNet R50-FPN、YOLO11s 与 YOLO11l 的历史单数据集训练和域内评估。完整七项实验记录、8 张表、5 幅图和来源定位见[三种模型测试](../../科研记录/三种模型测试.md)。本次整理日期为 2026-10-14；RetinaNet 原文记载队列于 2026-08-06 完成，YOLO 补充记录记载 2026-08-28—2026-08-29 运行。未连接服务器或重新训练。

主来源为 [Retinanet测试](../../牛只数据集/Retinanet测试.md)和 [yolo11SL](../../牛只数据集/yolo11SL.md)，[效率日志提取](../../牛只数据集/_效率数据_远程日志提取_20260908.md)用于时间线与 batch 补证，[7月工作](../../牛只数据集/7月工作.md)§13.6–13.7 用于重复图像审计。官方操作文档、版本源码及 Focal Loss 原论文用于方法核查，不证明历史远程实例的完整状态。

## 来源事实

- 两份主记录记载三模型各完成 14 集训练；两个 YOLO 各完成 14 集复评。RetinaNet 均在 val 上选取最佳 `bbox_mAP`，YOLO 在 Cows2021、diarycow 上用 test，其余 12 集用 val。
- RetinaNet 使用 MMDetection 3.3.0、PyTorch 2.1.0+cu121、FP32、物理 batch=2、累积8次、seed=0、保持宽高比的1333×800缩放设置；YOLO 使用 Ultralytics 8.4.92、PyTorch 2.5.1+cu124、AMP、seed=42、imgsz=640。输入、优化预算与随机性不同。
- 主文档训练batch表写16，示例命令写32；补充效率记录记载s/l用32、nbs=64。不能静默选择一个值代替全部run的有效配置。
- RetinaNet CImage val最佳0.694、末轮0.087；YOLO两个模型训练曲线峰值均为epoch1。现象明确，过拟合或优化不稳定的具体原因仍待逐轮和逐图证据。
- 既有审计记载diarycow train/test重复18张、train/val 4张、val/test 5张；NWAFU_CD train/val 5张、XGain 3张。没有成员交集清单，不能直接相加重叠数。

## 复算与综合

从文档展示读数复算，14域原协议mAP50–95宏平均为YOLO11s 0.7406、YOLO11l 0.7448、RetinaNet最佳val 0.7001；12个共同val子集分别为0.7177、0.7227、0.6754。12域分组只减少split差异，仍不是统一实现或匹配预算的架构比较。

YOLO11l在9/14域更高，原协议平均增加约0.42个百分点。RetinaNet最佳到末轮平均下降约5.43个百分点，其中CImage贡献下降量之和约79.9%；不据此推断所有域均严重过拟合。数字来自展示读数，精度受原文三/四位小数限制。

## 方法冲突与待核实

`yolo11SL.md`将best权重与峰值epoch差异归因于综合fitness；官方v8.4.92 `Metric.fitness()`权重为`[0,0,0,1]`，只使用mAP50–95。保留此冲突，需查历史安装源码、checkpoint epoch、EMA、并列峰值及复评条件。官方源码不是历史安装环境已核实的替代物。

YOLO汇总P/R来自F1工作点，不能写成固定conf=0.25结果。官方RetinaNet基础配置与COCO的预测数量上限提示需核对MooTrack360密集图像，但不直接证明项目实际配置或具体损失。

待核实项包括42个run身份、图片/标签hash、实际训练batch与输入张量、选模权重、有效后处理、重复成员、来源组隔离以及远程文件当前存在性。共同test、多seed不确定性、部署实测和跨数据集矩阵属于后续计划。

## 关联与归档

划分独立性背景见[数据集整理与独立测试评估来源摘要](cowcv-dataset-test-evaluation-evidence.md)。四架构与LODO的不同研究范围见[域内模型与架构比较来源摘要](cowcv-indomain-architecture-evidence.md)；本记录不将其结果混入本三模型表。

科研记录的assets目录保留CSV/JSON、可编辑表格、复算脚本、五份本地来源hash和十项外部来源清单。Study Image生成模型示意与表格母版，数值区程序排字。原始资料未改写，远程实验与SQLite/向量索引同步未运行。
