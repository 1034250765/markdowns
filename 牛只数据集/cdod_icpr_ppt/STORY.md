# CD-OD 组会汇报 PPT 叙事逻辑

## 主题
论文《Towards Robust Cross-Dataset Object Detection Generalization under Domain Specificity》组会汇报

## 目标受众
导师与同门，具备 CV/ML 基础

## 汇报目标
梳理论文如何提出"设置特异性"视角，解释跨数据集目标检测的退化规律，并说明其方法设计、关键实验与对我们研究的启示。

## 页数与结构（共 13 页）

### 01 封面
- 中文标题：面向领域特定性的跨数据集目标检测鲁棒泛化
- 英文标题：Towards Robust Cross-Dataset Object Detection Generalization under Domain Specificity
- 作者 / arXiv:2601.09497 / 汇报人 / 日期

### 02 目录
- 研究背景与动机
- 核心概念：Setting Specificity
- 实验设置与评估协议
- 定量结果
- 定性结果与讨论
- 结论与启示

### 03 研究背景与动机
- 目标检测在分布内表现好，但跨数据集急剧退化
- Waymo 事故引出部署现实：罕见遮挡、轨迹、环境弱覆盖
- 两个效应纠缠：视觉分布偏移 vs 标签分类法偏移
- 论文核心：把这两个效应拆开，量化各自贡献

### 04 核心概念：Setting Specificity
- 定义：按数据收集意图把数据集分为 setting-specific 与 setting-agnostic
- Setting-specific：单一操作环境、重复场景结构、一致视角、任务聚焦分类法（如 Cityscapes、BDD100K）
- Setting-agnostic：多场景、捕获条件变化大、标签空间广（如 COCO、Objects365）
- 人类研究验证：78 名参与者能稳定识别数据集场景签名
- 四种迁移模式：S→T，其中 S,T ∈ {specific, agnostic}

### 05 数据集与训练协议
- 四个数据集：COCO、Objects365、Cityscapes、BDD100K
- 统计对比：图像数、类别数、设置类型
- 训练：Faster R-CNN + ResNet-50 FPN，固定训练配方
- 每个源数据集训练一个模型，零样本跨数据集评估

### 06 评估协议：分离域偏移与标签不匹配
- Closed-label：仅评估共享标签交集，严格一对一映射
- Open-label：用 CLIP 把预测标签映射到最近目标标签，定位不变
- Near-miss 诊断：text-text 相似度、GT 排名、region-level 偏好边际
- 核心思想：闭标签 = 域偏移 + 标签不匹配；开标签 ≈ 仅域偏移

### 07 定量结果 I：闭标签跨数据集泛化
- 4×4 迁移矩阵（Table 3）
- 关键发现：Cityscapes 最可迁移；Objects365 最弱源；迁移强烈不对称
- Cityscapes 是最难目标，Objects365 是最易目标

### 08 定量结果 II：开标签评估
- 4×4 迁移矩阵（Table 4）
- 所有非对角线一致增益，但增益有界
- COCO→Objects365 +0.036；Objects365→COCO +0.036
- 但 COCO→Cityscapes/BDD 仍然很低 → 瓶颈在域偏移

### 09 定量结果 III：Near-miss 诊断
- Table 5：Objects365→BDD 41% near-miss，Cityscapes→COCO 仅 4%
- 区分"语义接近的错配"与"真正的语义混淆/域偏移"
- 阈值敏感性（Table 6）：τ=0.6 多数最佳

### 10 定性结果
- Figure 4：成功与失败案例对比
- 夜间、眩光等大域偏移场景退化最严重
- 印证 agnostic→specific 的鲁棒性悬崖

### 11 讨论：三大核心发现
1. Setting-specific 目标暴露"鲁棒性悬崖"：域偏移占主导
2. 跨数据集偏移是方向性的：不能视为对称
3. 标签不匹配真实但有界：开标签增益有限

### 12 结论、局限与未来工作
- 贡献：按设置特异性组织基准、完整训练-测试对、闭/开标签协议分离语义错位与视觉域偏移
- 局限：仅标准检测器；固定基准集合
- 未来：域适应策略、agnostic 与 specific 数据相互作用

### 13 对我们的研究的启示 / Q&A
- 牛只检测是典型 setting-specific 场景
- 从 COCO 迁移到牛只数据集属于 agnostic→specific，会面临鲁棒性悬崖
- 双向评估的重要性；标签对齐收益有限，应优先域适应/数据增广
- 论文评估协议可直接复用到我们的跨数据集评估

## 视觉风格
- 学术风：蓝白浅灰基底、思源黑体为主、公式与数据真实有据
- 优先使用论文原图（Fig.1-4、Table 3-6）作为 L1 主视觉证据
