---
id: cowcv-indomain-retest-october-evidence
type: source
status: draft
created: 2026-10-14
updated: 2026-10-14
sources:
  - 牛只数据集/10月域内重测计划.md
  - 牛只数据集/域内重测-10月.md
  - 牛只数据集/LODO测试-9月.md
  - 科研记录/实验记录格式参考.md
  - D:/牛只数据集实验/indomain_protocol.yaml
  - D:/牛只数据集实验/indomain_train.py
  - D:/牛只数据集实验/indomain_select_checkpoint.py
  - D:/牛只数据集实验/indomain_eval_test.py
  - D:/牛只数据集实验/indomain_compare_lodo.py
  - D:/牛只数据集实验/run_indomain_all.sh
  - D:/牛只数据集实验/indomain_seed_patch_test.py
  - https://docs.ultralytics.com/modes/train/
  - https://docs.ultralytics.com/modes/val/
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/data/build.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/utils/metrics.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/engine/trainer.py
  - https://github.com/pytorch/pytorch/blob/v2.5.1/docs/source/notes/randomness.rst
  - https://github.com/pytorch/pytorch/blob/v2.5.1/torch/utils/data/dataloader.py
  - https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py
  - https://arxiv.org/abs/2007.01434
  - https://arxiv.org/abs/1807.04975
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/nn/tasks.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/utils/torch_utils.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/cfg/default.yaml
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/models/yolo/detect/train.py
  - https://github.com/ultralytics/ultralytics/blob/v8.4.92/ultralytics/models/yolo/detect/val.py
---

# 牛只域内重测：10月统一协议、随机性审计与保持率核查

## 来源与成文范围

完整读取[10月重测计划](../../牛只数据集/10月域内重测计划.md)和[执行记录](../../牛只数据集/域内重测-10月.md)，补读[LODO记录](../../牛只数据集/LODO测试-9月.md)§2、§5.3–5.4，按[格式参考](../../科研记录/实验记录格式参考.md)整理为[科研记录：域内重测](../../科研记录/域内重测.md)。

历史主实验时段为2026-10-05至10-08，effective-seed扩展与汇总为10-09至10-12；本次整理日为2026-10-14。本页为来源核查摘要，不是新的实验事实来源。

本次另只读检查`D:/牛只数据集实验/`中7份协议与脚本镜像，并访问15项官方文档、版本源码及原论文入口。DomainBed和Terra Incognita只核查摘要与元信息，未精读全文。未连接远程服务器重取原CSV、日志、权重或预测；本地镜像与历史远程代码的身份一致性待核实。

## 来源明确记载的事实

- 范围为YOLO11m×14域；新数据train/val/test为25079/3142/3124，共31345图。四架构及YOLO11s/l不在本轮。
- 训练固定imgsz=640、100 epochs、batch=nbs=16、accumulate=1、AdamW@0.002、AMP、末批保留；初始化同一`lodo/yolo11m.pt`。历史环境为A100-PCIE-40GB、Ultralytics8.4.92、torch2.5.1+cu124。
- 按本域val AP50–95最高选模，并列较早；selected与epoch100分别在冻结test评测，完整一轮28条。
- 主表stock seed42 AP50–95宏平均0.7214；stock三轮11/14域记录为逐位一致，CBPD_ODD/COLO/HCRD有运行间差异。
- 10-06发生运行名遗漏导致部分主目录审计材料覆盖；原记录报告两域恢复的曲线、选模和test三重核验通过。本次看见本地运行名保护与输出隔离实现，未重审恢复原日志。
- effective-seed改变loader generator随机流，使用独立train_es42/43/44目录；原记录报告三种子宏平均0.72049±0.00159，样本SD、n=3。
- LODO分子三种子平均配主方案监督分母；逐域保持率宏平均约0.7328，原记录九组合口径0.7325。

## 本次复算与方法综合

[派生CSV](../../科研记录/域内重测.assets/逐域指标与种子结果.csv)摘录14域主表及es/LODO三种子；[复算JSON](../../科研记录/域内重测.assets/数值复算.json)保存显示精度算术与舍入边界。

AP50/AP50–95/P/R等权宏平均分别约0.9168/0.7214/0.9169/0.8838。逐域R平均0.7327588，而两个AP宏平均相除约0.6976，二者不可互换。CImage R约1.486，经验监督参照不是理论上限；高域内AP不足以保证高保持率，不能扩大为统计独立或无相关性。

stock三轮极差为CBPD_ODD0.00832、COLO0.00311、HCRD0.00924；HCRD加同seed判别后四次范围0.92850–0.94684，跨度0.01834。极差不用±SD写法。

固定8.4.92源码确认loader generator为固定常数，类名重映射机制、默认P/R的平滑F1峰值和fitness=[0,0,0,1]均可核查。由此区分stock运行重复与es有效种子重复；其适用边界限于记录所述配置。es跨seedSD仍可能叠加残余运行噪声，未严格分解方差。

## 冲突、限制与待核实

1. e*概括漏掉CID=75；采用8-calves=63、CID=75、其余83–100。靠后峰值不证明充分收敛。
2. 重测§6的0.734/0.729/0.735不是LODO AP；逐域复算约对应保持率。LODO AP宏平均约0.5056/0.5009/0.5034。
3. 两记录部分LODO SD字段不同，未确定字段转述原因；当前保持率表省略争议SD。LODO总体SD与es样本SD分别说明。
4. “10/14域SD≤0.004”受四位舍入影响；显示三值复算COCO约0.004012，严格计数9域，显示SD计数10域。不是主结论。
5. 主方案起止分钟相减11h02m，与原记录耗时11h01m差1分钟；照录且标注。
6. 默认P/R不等于固定conf=0.25严格计数；每预选权重一次评测不等于整个项目只读取test一次。
7. 小集合可能增加不确定性，但Google的291张不是最小test之一，不能把其波动单独归因于小样本。现有证据不证明CImage退化、设置特化或环境因素的唯一机制。

待执行项包括远程代码和权重身份、原始结果全覆盖、来源簇/近重复审计、固定部署工作点、嵌套seed重复、新视图单源14×14、匹配预算对照与四架构复核。本次未运行训练、推理、CPU seed机制测试、逐图归因、显著性检验或检索索引同步。

## 图表与关联

科研记录提供5幅正文图和10张表；Study Image制作流程图、随机性审计和表格视觉母版，表格数字由程序精确排字、统计图由Matplotlib绘制。原始资料未改写，来源hash及外部核查片段保存于同名assets目录。

参见[历史模型与架构来源核查](cowcv-indomain-architecture-evidence.md)及[数据整理与独立测试评估来源核查](cowcv-dataset-test-evaluation-evidence.md)，分别理解旧val表和历史数据准备边界。
