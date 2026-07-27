## MMDetection



**MMDetection** 是 OpenMMLab 基于 **PyTorch** 和 **MMEngine** 构建的目标检测工具箱，覆盖：

- 目标检测：Faster R-CNN、YOLOX、DINO、RTMDet 等
- 实例分割：Mask R-CNN、Mask2Former 等
- 旋转框、级联检测、多尺度训练与测试
- 自定义数据集、模型组件、损失函数和训练流程
- 分布式训练、混合精度、日志与可视化

它的核心特点是高度配置化，通常通过继承和修改 Python 配置文件来组合：



MMDetection 由 7 个主要部分组成，apis、structures、datasets、models、engine、evaluation 和 visualization。

- apis 为模型推理提供高级 API。

- structures 提供 bbox、mask 和 DetDataSample 等数据结构。

- datasets 支持用于目标检测、实例分割和全景分割的各种数据集。 **transforms** 包含各种数据增强变换。 **samplers** 定义了不同的数据加载器采样策略。

- **models** 是检测器最重要的部分，包含检测器的不同组件。

detectors 定义所有检测模型类。

data_preprocessors 用于预处理模型的输入数据。

backbones 包含各种骨干网络。

necks 包含各种模型颈部组件。

dense_heads 包含执行密集预测的各种检测头。

roi_heads 包含从 RoI 预测的各种检测头。

seg_heads 包含各种分割头。

losses 包含各种损失函数。

task_modules 为检测任务提供模块，例如 assigners、samplers、box coders 和 prior generators。

layers 提供了一些基本的神经网络层。

- **engine** 是运行时组件的一部分。

**runner** 为 [MMEngine 的执行器](https://mmengine.readthedocs.io/zh_CN/latest/tutorials/runner.html)提供扩展。

**schedulers** 提供用于调整优化超参数的调度程序。

**optimizers** 提供优化器和优化器封装。

**hooks** 提供执行器的各种钩子。

- **evaluation** 为评估模型性能提供不同的指标。
- **visualization** 用于可视化检测结果。

## 推理

```python
from mmdet.apis import DetInferencer

# 初始化模型
inferencer = DetInferencer('rtmdet_tiny_8xb32-300e_coco')
# 要用 MMDetection 的预训练模型进行推理，只需要把它的名字传给参数 model，权重将自动从 OpenMMLab 的模型库中下载和加载。
# 推理示例图片
inferencer('demo/demo.jpg', show=True)




# 在 MMDetection 中有一个非常容易的方法，可以列出所有模型名称。
models = DetInferencer.list_models('mmdet')


# 你可以通过将权重的路径或 URL 传递给 weights 来让推理器加载自定义的权重。
inferencer = DetInferencer(model='rtmdet_tiny_8xb32-300e_coco', weights='path/to/rtmdet.pth')

# 要加载自定义的配置和权重，你可以把配置文件的路径传给 model，把权重的路径传给 weights。
inferencer = DetInferencer(model='path/to/rtmdet_config.py', weights='path/to/rtmdet.pth')
```













## 数据集目录格式

```cmd
(ultralytics) [yxli@localhost 8-calves]$ tree -L 2
.
├── annotations
│   ├── instances_train.json
│   └── instances_val.json
└── images
    ├── train
    └── val

```







## 模型训练

