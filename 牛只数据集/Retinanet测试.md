# RetinaNet 牛只数据集测试过程与结果

## 1. 实验概况

| 项目 | 内容 |
|---|---|
| 任务 | 单类别牛只目标检测，类别名为 `cow` |
| 模型 | RetinaNet R50-FPN |
| 检测框架 | MMDetection 3.3.0 |
| 运行环境 | Python 3.10，PyTorch 2.1.0+cu121，CUDA 12.1 |
| GPU | NVIDIA A100-PCIE-40GB |
| 数据集数量 | 14 个 |
| 训练状态 | 14/14 全部完成 |
| 队列完成时间 | 2026-08-06 22:18:56 |
| 队列退出码 | `0` |

本实验记录的是每个数据集内部 `train/val` 划分上的同域验证结果，不是独立测试集结果，也不是跨数据集泛化结果。不同数据集的图像来源、场景、目标尺寸、标注密度和采集方式差异较大，因此 mAP 只适合在明确实验协议下比较。

## 2. 测试过程

### 2.1 远端项目与脚本

服务器：`yxli@211.69.141.71`

项目根目录：

```text
/data1/yxli/CODE/ultralytics/self_mAP
```

使用的训练入口：

```text
/data1/yxli/CODE/ultralytics/self_mAP/scripts/train_retinanet.py
/data1/yxli/CODE/ultralytics/self_mAP/scripts/run_retinanet_all.sh
```

批量脚本按固定顺序串行训练 14 个数据集，避免多个训练任务同时占用 GPU。训练日志和汇总结果分别保存在：

```text
/data1/yxli/CODE/ultralytics/self_mAP/logs/retinanet_14/100ep_ebs16
/data1/yxli/CODE/ultralytics/self_mAP/outputs/retinanet/100ep_ebs16
```

### 2.2 数据准备与检查

数据采用 COCO 格式标注，每个数据集统一为一个类别：

```text
categories = [{"id": 1, "name": "cow", "supercategory": "animal"}]
```

正式训练前，对 14 个数据集逐一执行预检，检查内容包括：

1. `instances_train.json` 和 `instances_val.json` 是否存在；
2. COCO 类别定义是否为单类 `cow`；
3. 图片目录是否存在、软链接是否有效；
4. 图片数量是否与 COCO JSON 中的 `images` 数量一致；
5. MMDetection `CocoDataset` 是否能够正常构建；
6. RetinaNet 有效配置是否能够生成。

14 个数据集均通过预检。数据规模如下，标注框数量来自 COCO JSON 中的 `annotations` 数量：

| 数据集 | 训练图像 | 训练框 | 验证图像 | 验证框 |
|---|---:|---:|---:|---:|
| 8-calves | 700 | 5,616 | 200 | 1,633 |
| animals_10 | 1,293 | 3,242 | 323 | 730 |
| CBPD_ODD | 292 | 423 | 73 | 92 |
| CID | 1,645 | 2,706 | 411 | 662 |
| CImage | 141 | 232 | 35 | 60 |
| COCO | 1,376 | 6,879 | 344 | 1,768 |
| COLO | 803 | 8,001 | 201 | 1,832 |
| Cows2021 | 7,248 | 9,395 | 1,023 | 1,238 |
| diarycow | 3,140 | 4,399 | 560 | 931 |
| Google Open Image | 2,333 | 9,952 | 583 | 2,341 |
| HCRD | 851 | 1,354 | 212 | 326 |
| MooTrack360 | 1,200 | 79,072 | 300 | 19,845 |
| NWAFU_CD | 1,503 | 7,413 | 375 | 1,793 |
| XGain | 1,326 | 6,039 | 331 | 1,613 |
| **合计** | **23,851** | **144,723** | **4,971** | **34,864** |

### 2.3 训练配置

| 项目 | 配置 |
|---|---|
| COCO 初始化 | RetinaNet R50-FPN COCO 预训练权重 |
| 训练轮数 | 100 epochs |
| 物理 batch size | 2 |
| 梯度累积 | 8 个 micro-batch |
| 有效 batch size | 16 |
| 精度 | FP32，AMP 关闭 |
| 优化器 | SGD |
| 初始学习率 | 0.01 |
| Momentum | 0.9 |
| Weight decay | 0.0001 |
| 学习率 warmup | 前 500 iterations，起始系数 0.001 |
| 学习率衰减 | 第 67 和 92 epoch 乘以 0.1 |
| 输入尺寸 | 保持宽高比缩放到 `1333 x 800` |
| 数据增强 | 随机水平翻转，概率 0.5 |
| DataLoader workers | 4 |
| 随机种子 | 0 |
| 验证频率 | 每个 epoch 验证一次 |
| 最优模型标准 | 最大化 `coco/bbox_mAP` |

由于 RetinaNet 在较大输入尺寸下显存占用较高，正式训练采用物理 batch 2 加梯度累积 8 次的方式，使有效 batch 保持为 16。训练过程中显存占用约 2.5--3.9 GB，没有出现显存溢出。

### 2.4 评估方式

每个 epoch 在对应数据集的 `val` 划分上执行 COCO bbox 评估，记录以下指标：

- `mAP`：IoU 0.50--0.95 的平均精度，即 `coco/bbox_mAP`；
- `mAP50`：IoU=0.50 时的平均精度，即 `coco/bbox_mAP_50`；
- 同时记录 `mAP75`、小/中/大目标 AP 和 precision 等辅助指标。

每个数据集都会保存：

```text
epoch_N.pth
best_coco_bbox_mAP_epoch_N.pth
last_checkpoint
```

如果中途停止，重新启动批量脚本时会读取 `last_checkpoint`，已完成的数据集会跳过，当前数据集从最近保存的 epoch checkpoint 继续训练。

### 2.5 Smoke test

正式批量训练前，在 `CImage` 上进行了 1 epoch 的真实 GPU smoke test，用于验证模型初始化、COCO 预训练权重下载、单类检测头、训练、验证和 checkpoint 保存链路。该 smoke test 得到：

```text
mAP50-95 = 0.535
mAP50    = 0.666
```

该结果只用于验证代码链路，不纳入下面的 100 epoch 正式结果。

## 3. 正式测试结果

下表中的“最佳”表示 100 个 epoch 中验证集 `mAP50-95` 最高的 epoch；“最终”表示第 100 epoch 的结果。

| 数据集 | 最佳 epoch | 最佳 mAP50-95 | 最佳 mAP50 | 最终 mAP50-95 | 最佳 checkpoint |
|---|---:|---:|---:|---:|---|
| 8-calves | 9 | 0.536 | 0.966 | 0.504 | `best_coco_bbox_mAP_epoch_9.pth` |
| animals_10 | 3 | 0.597 | 0.846 | 0.597 | `best_coco_bbox_mAP_epoch_3.pth` |
| CBPD_ODD | 68 | 0.947 | 0.999 | 0.943 | `best_coco_bbox_mAP_epoch_68.pth` |
| CID | 11 | 0.861 | 0.975 | 0.850 | `best_coco_bbox_mAP_epoch_11.pth` |
| CImage | 3 | 0.694 | 0.946 | 0.087 | `best_coco_bbox_mAP_epoch_3.pth` |
| COCO | 5 | 0.461 | 0.717 | 0.457 | `best_coco_bbox_mAP_epoch_5.pth` |
| COLO | 16 | 0.605 | 0.922 | 0.571 | `best_coco_bbox_mAP_epoch_16.pth` |
| Cows2021 | 63 | 0.837 | 0.989 | 0.833 | `best_coco_bbox_mAP_epoch_63.pth` |
| diarycow | 69 | 0.860 | 0.990 | 0.856 | `best_coco_bbox_mAP_epoch_69.pth` |
| Google Open Image | 7 | 0.449 | 0.742 | 0.426 | `best_coco_bbox_mAP_epoch_7.pth` |
| HCRD | 80 | 0.919 | 0.979 | 0.918 | `best_coco_bbox_mAP_epoch_80.pth` |
| MooTrack360 | 28 | 0.537 | 0.841 | 0.515 | `best_coco_bbox_mAP_epoch_28.pth` |
| NWAFU_CD | 31 | 0.688 | 0.884 | 0.676 | `best_coco_bbox_mAP_epoch_31.pth` |
| XGain | 71 | 0.811 | 0.975 | 0.809 | `best_coco_bbox_mAP_epoch_71.pth` |

### 3.1 宏平均统计

以下为 14 个数据集等权宏平均，不按图像数或标注框数加权：

| 指标 | 数值 |
|---|---:|
| 最佳 mAP50-95 宏平均 | 0.7001 |
| 最佳 mAP50 宏平均 | 0.9122 |
| 第 100 epoch mAP50-95 宏平均 | 0.6459 |
| 最佳到最终的平均下降 | 0.0543 |

## 4. 结果分析

1. `CBPD_ODD` 的最佳 mAP50-95 最高，为 `0.947`；`HCRD`、`diarycow`、`CID`、`Cows2021` 和 `XGain` 也达到 `0.811` 以上。
2. `Google Open Image` 和 `COCO` 的最佳 mAP50-95 相对较低，分别为 `0.449` 和 `0.461`，说明当前模型在这两个验证划分上的定位或场景适应难度更高。
3. `CImage` 在第 3 epoch 达到 `0.694`，但第 100 epoch 下降到 `0.087`，存在明显的后期过拟合或训练不稳定现象。后续使用时必须采用最佳 checkpoint，而不是 `epoch_100.pth`。
4. 多数数据集在较早 epoch 已达到最佳值，说明 100 epoch 对部分小规模或较简单数据集偏长；后续可以考虑早停、按数据集设置训练轮数，或根据验证集曲线调整学习率策略。
5. MooTrack360 的标注框数量明显高于其他数据集，但宏平均没有按标注框数量加权，避免单一大数据集主导总体结论。不同数据集之间仍不能简单理解为模型能力的绝对排名。

## 5. 结果和 checkpoint 位置

完整结果汇总：

```text
/data1/yxli/CODE/ultralytics/self_mAP/logs/retinanet_14/100ep_ebs16/summary.log
```

正式输出根目录：

```text
/data1/yxli/CODE/ultralytics/self_mAP/outputs/retinanet/100ep_ebs16
```

例如，XGain 的最佳权重为：

```text
/data1/yxli/CODE/ultralytics/self_mAP/outputs/retinanet/100ep_ebs16/XGain/best_coco_bbox_mAP_epoch_71.pth
```

## 6. 结论与后续建议

本次 RetinaNet R50-FPN 实验在统一单类别 `cow`、统一 100 epoch 和统一 COCO bbox 评估口径下，完成了 14 个牛只数据集的同域验证。最佳 mAP50-95 的 14 数据集等权平均为 `0.7001`，最佳 mAP50 等权平均为 `0.9122`。

后续跨数据集泛化实验应固定使用每个数据集的最佳 checkpoint，建立训练集到其他数据集验证集的交叉评估矩阵，而不能把本报告中的同域验证 mAP 直接当作跨域性能。对于 `CImage` 等后期性能明显下降的数据集，建议优先检查早停策略、学习率衰减和训练/验证划分是否存在分布或重复样本问题。
