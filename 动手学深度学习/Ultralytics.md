##  Ultralytics



​    Ultralytics是一个开源的计算机视觉和深度学习框架，旨在简化训练、评估和部署视觉模型的过程。该框架提供了一系列流行的视觉模型，包括YOLOv5 、YOLOv4、YOLOv3、YOLOv3-tiny、YOLOv5-tiny、EfficientDet、PAN、PP-YOLO等，并提供了训练、评估和推理的工具和实用程序。


**Ultralytics框架的一些主要特点包括：**

简单易用：Ultralytics提供了简洁的API和命令行工具，使用户可以轻松地训练、评估和部署视觉模型。
多种视觉模型支持：Ultralytics支持多种流行的目标检测和图像分割模型，用户可以根据自己的需求选择合适的模型进行训练和部署。
高性能：Ultralytics框架基于PyTorch深度学习框架，具有优秀的性能和灵活性，同时提供了一系列优化和加速的功能，可加快训练和推理速度。
开源社区支持：Ultralytics是一个开源项目，拥有活跃的开发者社区，用户可以在GitHub上查看源代码、提交问题和贡献代码。

### YOLO 中有哪些不同的模式？[#](https://docs.ultralytics.com/zh/usage/python#yolo-中有哪些不同的模式)

Ultralytics YOLO 提供了各种模式来满足不同的 [机器学习](https://www.ultralytics.com/glossary/machine-learning-ml) 工作流需求。这些包括：

- **[训练 (Train)](https://docs.ultralytics.com/zh/modes/train)**：使用自定义数据集训练模型。
- **[验证 (Val)](https://docs.ultralytics.com/zh/modes/val)**：在验证集上验证模型性能。
- **[预测 (Predict)](https://docs.ultralytics.com/zh/modes/predict)**：对新图像或视频流进行预测。
- **[导出 (Export)](https://docs.ultralytics.com/zh/modes/export)**：将模型导出为 ONNX 和 TensorRT 等各种格式。
- **[追踪 (Track)](https://docs.ultralytics.com/zh/modes/track)**：视频流中的实时对象追踪。
- **[基准测试 (Benchmark)](https://docs.ultralytics.com/zh/modes/benchmark)**：针对不同配置对模型性能进行基准测试。







datasets文件夹：**包含数据集的配置文件，如数据路径、类别信息等（就是我们训练YOLO模型的时候需要一个数据集，这里面就保存部分数据集的yaml文件，如果我们训练的时候没有指定数据集则会自动下载其中的数据集文件，**但是很容易失败！**）。

```makefile



**models文件夹：**存放模型配置文件，定义了模型结构和训练参数等。

models文件夹中的每个.yaml文件代表了不同的YOLOv8模型配置，具体包括：
 **yolov8.yaml:**  这是YOLOv8模型的标准配置文件，定义了模型的基础架构和参数。
 **yolov8-cls.yaml:** 配置文件调整了YOLOv8模型，专门用于图像分类任务。
 **yolov8-ghost.yaml:** 应用Ghost模块的YOLOv8变体，旨在提高计算效率。
 **yolov8-ghost-p2.yaml 和 yolov8-ghost-p6.yaml:** 这些文件是针对特定大小输入的Ghost模型变体配置。
 **yolov8-p2.yaml和 yolov8-p6.yaml:** 针对不同处理级别（例如不同的输入分辨率或模型深度）的YOLOv8模型配置。
 **yolov8-pose.yaml:** 为姿态估计任务定制的YOLOv8模型配置。
 **yolov8-pose-p6.yaml:** 针对更大的输入分辨率或更复杂的模型架构姿态估计任务。
 **yolov8-rtdetr.yaml:** 可能表示实时检测和跟踪的YOLOv8模型变体。
 **yolov8-seg.yaml 和 yolov8-seg-p6.yaml:** 这些是为语义分割任务定制的YOLOv8模型配置。
 这些配置文件是模型训练和部署的核心，同时大家如果进行改进也是修改其中的对应文件来优化 网络结构。
 
 **trackers文件夹：**用于追踪算法的配置。
 **__init__.py文件：**表明`cfg`是一个Python包。
 **default.yaml：**项目的默认配置文件，包含了被多个模块共享的通用配置项。【设置task、mode、data、epochs、patience、batch、imgsz、resume】

```

**在data/scripts文件夹中，包括了一系列脚本和Python文件：**

```PYTHON

 
 \- download_weights.sh: 用来下载预训练权重的脚本。
 \- get_coco.sh, get_coco128.sh, get_imagenet.sh: 用于下载COCO数据集完整版、128张图片版以及ImageNet数据集的脚本。
 
 **在data文件夹中，包括：**
 
 **annotator.py:** 用于数据注释的工具。
 **augment.py:** 数据增强相关的函数或工具。
 **base.py, build.py, converter.py:** 包含数据处理的基础类或函数、构建数据集的脚本以及数据格式转换工具。
 **dataset.py:** 数据集加载和处理的相关功能。
 **loaders.py:** 定义加载数据的方法。
 **utils.py:** 各种数据处理相关的通用工具函数

```



**engine文件夹包含与模型训练、评估和推理有关的核心代码：**

```python

 
 **exporter.py:** 用于将训练好的模型导出到其他格式，例如ONNX或TensorRT。
 **model.py:** 包含模型定义，还包括模型初始化和加载的方法。
 **predictor.py:** 包含推理和预测的逻辑，如加载模型并对输入数据进行预测。
 **results.py:** 用于存储和处理模型输出的结果。
 **trainer.py:** 包含模型训练过程的逻辑。
 **tuner.py:** 用于模型超参数调优。
 **validator.py:** 包含模型验证的逻辑，如在验证集上评估模型性能。

```

 **hub文件夹通常用于处理与平台或服务集成相关的操作，包括：**

 **auth.py:** 处理认证流程，如API密钥验证或OAuth流程。
 **session.py:** 管理会话，包括创建和维护持久会话。
 **utils.py:** 包含一些通用工具函数，可能用于支持认证和会话管理功能。



 **models/yolo目录中包含了YOLO模型的不同任务特定实现：**

 **classify:** 这个目录可能包含用于图像分类的YOLO模型。
 **detect:** 包含用于物体检测的YOLO模型。
 **pose:** 包含用于姿态估计任务的YOLO模型。
 **segment:** 包含用于图像分割的YOLO模型，

 **modules文件夹:**
   **__init__.py:** 表明此目录是Python包。
   **block.py:** 包含定义神经网络中的基础块，如残差块或瓶颈块。
   **conv.py:** 包含卷积层相关的实现。
   **head.py:** 定义网络的头部，用于预测。
   **transformer.py:** 包含Transformer模型相关的实现。
   **utils.py:** 提供构建神经网络时可能用到的辅助函数。

 **__init__.py:** 同样标记这个目录为Python包。

 **autobackend.py:** 用于自动选择最优的计算后端。

 tasks.py: 定义了使用神经网络完成的不同任务的流程，例如分类、检测或分割，所有的流程基本上都定义在这里，定义模型前向传播都在这里。
![img](https://i-blog.csdnimg.cn/blog_migrate/99c221f3a5077b54b75df26f46cdf1a9.png)





## 使用预训练 模型进行推理



**单张图片**

```python
from ultralytics import YOLO

# 加载预训练模型 (YOLOv8)
model = YOLO('yolov8n.pt')  # 可以替换为 yolov8s.pt, yolov8m.pt 等不同大小的模型

# 进行预测
results = model('https://ultralytics.com/images/bus.jpg')  # 预测单张图片

# 显示结果
results[0].show()

# 保存结果
results[0].save('result.jpg')


```

### Ultralytics 的 `model.predict()` 支持一次传入多张图片组成的列表。

```python
imgs = [c[0] for c in chunk]
results = model.predict(
    imgs,
    conf=CONF,
    imgsz=IMGSZ,
    device=DEVICE,
    batch=len(imgs),
    stream=False,
)
```

这里的 `imgs` 是图片路径列表：

```python
[
    "/path/0001.jpg",
    "/path/0002.jpg",
    "/path/0003.jpg",
]
```

`model.predict()` 会对列表里的所有图片进行批量推理，并返回与输入顺序对应的结果列表：

`stream=False` 表示：等待这一批图片全部推理完成，并把全部结果一次性返回为列表。

`outs` 是当前这一批图片对应的标签输出路径列表。

**训练自定义模型 **

```python
from ultralytics import YOLO

# 加载基础模型
model = YOLO('yolov8n.pt')  # 也可以直接使用 'yolov8n.yaml' 从头开始训练

# 训练模型
results = model.train(
    data='coco128.yaml',  # 数据集配置文件
    epochs=100,          # 训练轮数
    imgsz=640,           # 输入图像大小
    batch=16,            # 批量大小
    name='yolov8n_custom'  # 实验名称
)

model.train(
    data="/root/RUN-CODE/COWBenchmark/yamls/XGain_single.yaml",
    epochs=50, imgsz=640, batch=128, device=0, workers=8,
    project="/root/RUN-CODE/COWBenchmark/runs",
    name="XGain_single",
    exist_ok=True, amp=False,
)

results = model.train(resume=True) 恢复训练


model.train() 方法训练完成后，返回的是一个 ultralytics.utils.metrics.DETECTION_METRICS_MAP 对应的评估指标对象。

Metrics 评估指标对象
具体来说，根据你训练的任务类型不同，返回的对象类型也不同：

目标检测任务 (Detection)：返回的是 DetMetrics 对象。

实例分割任务 (Segmentation)：返回的是 SegMetrics 对象。

姿态估计任务 (Pose)：返回的是 PoseMetrics 对象。

图像分类任务 (Classification)：返回的是 ClassifyMetrics 对象。
results = model.train(data="coco8.yaml", epochs=10)

# 1. 获取 mAP50-95 (最主要的综合指标)
print(results.box.map)      # 或者是 results.results_dict['metrics/mAP50-95(B)']

# 2. 获取 mAP50
print(results.box.map50)    # 或者是 results.results_dict['metrics/mAP50(B)']

# 3. 获取 mAP75
print(results.box.map75)

# 4. 获取精确率 (Precision) 和 召回率 (Recall)
print(results.box.mp)       # 平均精确率 (Mean Precision)
print(results.box.mr)       # 平均召回率 (Mean Recall)

# 5. 获取一个包含所有核心指标的字典
print(results.results_dict)
```

**验证数据集**

```python
from ultralytics import YOLO

# Load a YOLO model
model = YOLO("yolo26n.yaml")

# Train the model
model.train(data="coco8.yaml", epochs=5)

# Validate on separate data
model.val(data="path/to/separate/data.yaml")
```



**数据集yaml**

```yaml
names:
- cow
nc: 1
path: /root/RUN-CODE/COWBenchmark/data/8-Calves_test
train: images/
val: images/
```

**导出**



```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")
model.export(format="onnx", dynamic=True)
```

**追踪**

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")  # load an official detection model
model = YOLO("yolo26n-seg.pt")  # load an official segmentation model
model = YOLO("path/to/best.pt")  # load a custom model

# Track with the model
results = model.track(source="https://youtu.be/LNwODJXcvt4", show=True)
results = model.track(source="https://youtu.be/LNwODJXcvt4", show=True, tracker="bytetrack.yaml")
```



**使用训练器trainer**

`YOLO` 模型类充当了 Trainer 类的高级封装。每个 YOLO 任务都有自己的训练器，它们都继承自 `BaseTrainer`。这种架构允许在你的 [机器学习工作流](https://docs.ultralytics.com/guides/model-training-tips) 中实现更大的灵活性和定制化。

```python
from ultralytics.models.yolo.detect import DetectionTrainer

# 定义你的训练配置
options = {
    "model": "yolov8n.pt",  # 1. 这里指定模型！可以是预训练权重，也可以是 'yolov8n.yaml' 不带权重训练
    "data": "coco8.yaml",    # 2. 指定数据集配置文件
    "epochs": 10,            # 3. 训练轮数
    "imgsz": 640,            # 4. 图片输入大小
    "batch": 16,             # 5. 批次大小
}

# 实例化并传入配置
trainer = DetectionTrainer(overrides=options)
trainer.train()

# 训练完成后获取最佳模型路径
trained_model_path = trainer.best
```

```python
from ultralytics.models.yolo.detect import DetectionPredictor, DetectionTrainer, DetectionValidator

# trainer
trainer = DetectionTrainer(overrides={})
trainer.train()
trained_model = trainer.best

# Validator
val = DetectionValidator(args=...)
val(model=trained_model)

# predictor
pred = DetectionPredictor(overrides={})
pred(source=SOURCE, model=trained_model)

# resume from last weight
overrides["resume"] = trainer.last
trainer = DetectionTrainer(overrides=overrides)
```

