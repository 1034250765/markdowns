# CowCV 候选数据集初筛 · Ruchay 2026 补充材料 134 条

> 对 Ruchay et al. 2026 综述补充材料 Annex 3/4 中**全部 134 条牛只数据集记录**，按 CowCV 检测视图硬约束做的**桌面初筛**。结果：**P0 直接纳入候选 12 条、P1 转换后可纳入 31 条、P2 信息不足待核 36 条、X 不兼容 55 条**。

> ⚠️ **本表是初筛，不是结论**。所有判断只基于附表的文字描述，**未访问任何数据集页面、未下载任何数据、未核验任何许可证**。134 条全部带 `许可待核`；P0/P1 必须完成网页核验与样本抽检后才能升级为"纳入"。

> ⚠️ **数据源本身有质量问题**（已修正）：原附表 Beef/Dairy 两 sheet 中 41 行的 `AI Task Category` 与 `Imaging environment` 两列内容被整列互换；另有跨行合并单元格导致 12 条 `env`、9 条 `size` 的**假缺失**。修正记录见附录 B。

- **`cowcv_ruchay2026_screening.csv`** —— 完整 22 列标签表（UTF-8 BOM，Excel 直接打开）在本目录下。

---

## 1. 本次初筛怎么做的

### 1.1 数据来源

Ruchay et al. 2026（*Computers and Electronics in Agriculture* 250:111917）的 Elsevier 补充材料：

| 文件                   | 内容                     | 本次用到的 sheet              |
| -------------------- | ---------------------- | ------------------------ |
| `mmc3.xlsx`（Annex 3） | 论文来源汇总表，8 列            | `Beef` 46 条、`Dairy` 45 条 |
| `mmc4.xlsx`（Annex 4） | 仓库来源汇总表，10 列（多 `Year`） | `Cattle` 43 条            |

> 该综述正文声称牛只数据集共 131 条，**附件实测 134 条**（差 3，未明原因）。本表以附件实测为准。

### 1.2 打标规范

判定依据来自 CowCV 的正式文档（`文章初稿.md` §2.2 / §3.1 / §3.2 / §3.3），核心约束：

| 维度 | 要求 |
|---|---|
| 类别 | 单类 `cow`，原始多类须合并 |
| 框语义 | **整牛水平框（HBB）**。局部特写（脸/鼻纹/眼/视网膜）、部位框、关键点外接框、掩膜外接矩形**均不可**直接使用 |
| 格式 | YOLO 归一化 `class_id x_center y_center width height` |
| 规模 | 非硬阈值，但 **<220 张**已有排除先例（PASCAL VOC cow 217、Animal-Pose ~200、AP-10K ~200、Animal Image 60）；CImage 176 张是特例 |
| 来源独立性 | 与已纳入 14 项同源或近重复的不重复计入 |
| 许可 | 许可证与再分发范围须逐项核验 |

**已纳入的 14 项基准**：Cows2021、Dairy Cow、8-calves、COLO、MooTrack360、XGain、CID、HCRD、NWAFU Cattle Dataset、animals_10、CImage、COCO cow subset、Google Open Images cow subset、CBPD_ODD。

**等级定义**：

| 等级 | 含义 |
|---|---|
| **P0** | 直接纳入候选 —— 原生整牛框 + 图像数 ≥300 + 无局部化风险 |
| **P1** | 转换/重标后可纳入 —— 需转旋转框、合并类别，或牛体可见但需补画整牛 HBB |
| **P2** | 信息不足待核 —— 字段缺失或含糊，无法判定 |
| **X** | 不兼容 —— 框语义红线 / 无检测框 / 规模过小 / 已知同源 |

> **P1 与 X 的分界线是「牛体是否可见」，不是「有没有框」**。图像里牛体完整可见、只是标注为图像级分类的属 P1（可补画框）；牛脸/鼻纹特写这类牛体不在画面内的属 X。

### 1.3 执行流程

134 条按原始 sheet 分三片（Beef 46 / Dairy 45 / Cattle 43），每片由独立子智能体按同一份规范逐条打标，再合并、去重、交叉分析。每条结果都要求给出 `evidence`（引用附表原文片段）与 `confidence`，信息不足处一律标 P2/不确定，不得臆测。

---

## 2. 总览

| 等级 | 条数 | 占比 | 含义 |
|---|---:|---:|---|
| **P0** | **11** | 8% | 直接纳入候选 |
| **P1** | **31** | 23% | 转换/重标后可纳入 |
| **P2** | **36** | 27% | 信息不足待核 |
| **X** | **56** | 42% | 不兼容 |
| 合计 | 134 | 100% | |

**按来源片**：

| 片 | 条数 | P0 | P1 | P2 | X |
|---|---:|---:|---:|---:|---:|
| Beef（论文来源·肉牛） | 46 | 8 | 5 | 12 | 21 |
| Dairy（论文来源·奶牛） | 45 | 2 | 16 | 5 | 22 |
| Cattle（仓库来源） | 43 | 1 | 10 | 19 | 13 |

**原始框语义分布**：

| box_semantics | 条数 |
|---|---:|
| `no_box` | 51 |
| `whole_animal_hbb` | 29 |
| `mask_or_kpt_only` | 28 |
| `body_part` | 19 |
| `unclear` | 5 |
| `native_obb` | 2 |

**风险标签**（可多选）：

| 风险 | 条数 |
|---|---:|
| `许可待核` | 134 |
| `框语义待核` | 41 |
| `需重标` | 38 |
| `帧冗余` | 30 |
| `规模偏小` | 14 |
| `非牛混入` | 12 |
| `同源待核` | 11 |
| `实例密度低` | 3 |
| `标注质量不达标` | 1 |

**判断置信度**：{'high': 54, 'medium': 53, 'low': 27}

> 关键读法：`no_box`（51 条）+ `body_part`（19 条）合计 70 条 = 52%，**超过一半的牛只数据集根本不提供整牛检测框**。这是 CowCV 扩充候选池时最硬的约束。

---

## 3. P0 · 直接纳入候选（11 条）

> 这些条目在附表中**已明确提供整牛检测框**、规模达标、无局部化风险，是优先核验对象。
> ⚠️ 仍须完成：① 网页可达性与许可核验；② 抽样确认框语义确为整牛；③ 与已纳入 14 项做近重复审计。
>
> ⚠️ **其中 8 条来自连续视频帧，须先按来源序列分层抽样**，否则帧间高度相关会污染训练/验证划分：`C005`、`C011`、`C024`、`C026`、`C031`、`C038`、`C073`、`C091`

| id     | 数据集                                                            |     图像数 | 视角 / 环境       | 风险                 | 判断依据（附表原文）                                                 |
| ------ | -------------------------------------------------------------- | ------: | ------------- | ------------------ | ---------------------------------------------------------- |
| `C005` | CVB dataset (Zia et al., 2023)                                 | 225,900 | 地面侧视 / 实验受控   | 许可待核 · 帧冗余 · 实例密度低 | Eleven visually perceptible behaviors per cattle, bounding |
| `C010` | BR Cattle Dataset (Soares et al., 2021)                        |   5,058 | 航拍高空 / 户外草场   | 许可待核               | Manually delineated bounding boxes labeled as "cattle" cla |
| `C011` | Cattle Detection Dataset (Wu et al., 2024)                     |   6,529 | 高位斜俯视 / 半开放牛场 | 许可待核 · 帧冗余         | 6,529 frames featuring 26,420 cattle instances; manual aud |
| `C020` | Beef Cattle dataset (Zhang, 2026)                              |  16,889 | 高位斜俯视 / 半开放牛场 | 许可待核               | Object Detection, Keypoint Detection, Re-identification; B |
| `C024` | Beef Cattle Behavior Recognition Dataset (Cao et al., 2025)    |   2,000 | 高位斜俯视 / 室内牛舍  | 许可待核 · 帧冗余         | Target Detection, Target Tracking; 2000 target detection i |
| `C026` | Dataset for Cattle Behavior Analysis 1.0 (Ahmed et al., 2025)  |  92,592 | 高位斜俯视 / 半开放牛场 | 许可待核 · 帧冗余         | 92,592 labeled video frames; Bounding boxes around cattle, |
| `C031` | Multi-camera Multi-cow Tracking Dataset (Xu et al., 2025a)     |   4,253 | 多视角 / 半开放牛场   | 许可待核 · 帧冗余         | 48 videos, 4,253 images for detection; Cow detection using |
| `C038` | Cattle Movement and Behavior Dataset (Lopez et al., 2025)      |  39,364 | 高位斜俯视 / 户外草场  | 许可待核 · 帧冗余         | 39,364 annotated frames; Bounding boxes for "bovine", nine |
| `C073` | MmCows: A Multimodal Dataset for Dairy Cattle Monitoring (Choi |  20,000 | 不确定 / 不确定     | 许可待核 · 帧冗余         | 20,000 annotated images; Cow identification (bounding boxe |
| `C091` | OTB-Cow dataset (Wang et al., 2025c)                           |  24,430 | 不确定 / 半开放牛场   | 许可待核 · 帧冗余         | 1716 images, 24430 image frames; LabelImg and DarkLabel    |
| `C109` | Drone images and their annotations of grazing cows             |   1,385 | 航拍高空 / 户外草场   | 许可待核               | 1385 images, 4941 bounding boxes；PASCAL_VOC1.1 and YOLO_V1 |

---

## 4. P1 · 转换 / 重标后可纳入（31 条）

> 需做转换或补画框。按处理动作分类：
> - **需重标**：牛体可见但原标注是图像级分类/掩膜/关键点 → 补画整牛 HBB
> - **需类别合并**：原始多类 → 合并为单类 `cow`
> - **需转框**：旋转框 OBB → HBB

| id | 数据集 | 图像数 | 视角 / 环境 | 风险 | 判断依据 |
|---|---|---:|---|---|---|
| `C003` | Beef identify dataset (Qiao et al., 2021) | 14,520 | 不确定 / 半开放牛场 | 许可待核 · 需重标 · 帧冗余 | 50 individual beef cattle, 363 videos, approx. 14,520 RGB  |
| `C006` | RecBov51c dataset (Weber et al., 2020) | 27,849 | 不确定 / 半开放牛场 | 许可待核 · 需重标 · 帧冗余 | 51 individual Pantaneira cattle, 27,849 AHD 720p images; I |
| `C033` | UAV-based LiDAR and RGB Cattle Dataset (Wang et al., 2025a) | 3,823 | 不确定 / 半开放牛场 | 许可待核 · 框语义待核 | 3,823 RGB images, 173 UAV images, 38 point clouds; Agisoft |
| `C036` | Cattle Grazing Behavior and Vegetation Dynamics Dataset (Wang  | 4,140 | 航拍高空 / 户外草场 | 许可待核 · 需重标 | Estimated 4140 multispectral images; observer-recorded ann |
| `C042` | Cattle Weight Estimation Dataset (Bai et al., 2025a) | 3,950 | 多视角 / 室内牛舍 | 许可待核 · 需重标 | RGB image data (side views, rear views); Colored paint mar |
| `C047` | Holstein Cattle Side-View Benchmark Dataset (Bhole et al., 201 | 1,237 | 地面侧视 / 室内牛舍 | 许可待核 · 需重标 | 136 individual Holstein cows, 1237 unique pairs |
| `C048` | Holstein cattle side-view RGB-thermal dataset (Bhole et al., 2 | 3,694 | 地面侧视 / 室内牛舍 | 许可待核 · 需重标 | 383-class cow identity labels; segmentation masks |
| `C051` | Cattle Pose Estimation Dataset (Li et al., 2019) | 2,134 | 地面侧视 / 户外草场 | 许可待核 · 需重标 · 帧冗余 · 同源待核 | 2134 RGB images from 219 MOV videos; 16 body keypoints |
| `C052` | Multicow pose estimation dataset (Gong et al., 2022) | 1,800 | 高位斜俯视 / 半开放牛场 | 许可待核 · 需重标 · 帧冗余 · 框语义待核 | 1800 annotated images; tight bounding boxes + keypoints |
| `C053` | Cow-AMS Behavior dataset (Koskela et al., 2022) | 1,700,660 | 高位斜俯视 / 室内牛舍 | 许可待核 · 需重标 · 帧冗余 · 实例密度低 | 1,700,660 valid labeled images; Manual per-frame labeling |
| `C054` | Raramuri Criollo cattle body condition score dataset (Winkler  | 5,940 | 顶部俯视 / 户外草场 | 许可待核 · 需重标 · 帧冗余 | 5940 RGB+depth image pairs; BCS by expert judges |
| `C055` | MultiviewC dataset (Ma et al., 2024) | 3,920 | 多视角 / 实验受控 | 许可待核 · 框语义待核 | Ground truth for 2D localization and 3D detection, oriente |
| `C064` | CowXNet dataset (Lodkaew et al., 2022) | 2,000 | 顶部俯视 / 半开放牛场 | 许可待核 · 框语义待核 · 帧冗余 | 2,000 RGB TIFF images; expert boxes and key-points |
| `C066` | Longitudinal dairy cow body weight prediction dataset (Bi et a | 40,405 | 顶部俯视 / 室内牛舍 | 许可待核 · 需重标 · 帧冗余 · 框语义待核 | 40,405 depth images; manual cow contour labeling via Label |
| `C074` | MultiCamCows2024 (Yu et al., 2025) | 101,329 | 多视角 / 室内牛舍 | 许可待核 · 同源待核 · 框语义待核 · 帧冗余 | cropped cow torsos; COCO annotations for cow detection |
| `C076` | Lameness Detection Dataset (Russello et al., 2024) | 62,000 | 地面侧视 / 半开放牛场 | 许可待核 · 需重标 · 帧冗余 · 框语义待核 | 272 videos (~62,000 frames); 9 keypoints via T-LEAP |
| `C077` | Dairy Cow Lameness Hierarchy Dataset (Sheng et al., 2025) | — | 地面侧视 / 不确定 | 许可待核 · 需重标 · 帧冗余 | 1046 videos from 85 dairy cows; Gait scores by 5 assessors |
| `C083` | Dairy Cow Behavioral Phenotypes Dataset (Inadagbo et al., 2024 | — | 高位斜俯视 / 室内牛舍 | 许可待核 · 需重标 · 帧冗余 | 3584 video recordings (24h footage); Segment Anything Mode |
| `C087` | Multi-animal Cattle Pose Estimation Dataset (Perneel et al., 2 | 12,500 | 不确定 / 室内牛舍 | 许可待核 · 需重标 · 帧冗余 | 500 train/val frames + 12,000 test frames; keypoints |
| `C088` | Holstein Dairy Cow Depth Image Dataset (Chiang et al., 2025) | 9,600 | 不确定 / 不确定 | 许可待核 · 需重标 · 框语义待核 | 9600 raw depth images; YOLOX object detection for cows |
| `C089` | Multi-method Dairy Cattle Body Condition Score Dataset (Swartz | 493 | 地面侧视 / 不确定 | 许可待核 · 需重标 · 规模偏小 | 493 unique images (986 photo sets); human BCS scoring |
| `C092` | Indian Cattle Image Dataset | 12,000 | 不确定 / 不确定 | 许可待核 · 需重标 | Breed Classification, Identification；size: ~12,000–15,000  |
| `C095` | Cattle Weight Detection Model + Dataset (12k~) | 12,000 | 不确定 / 不确定 | 许可待核 · 需重标 | Weight Detection；size: 12,000+ images (from 16,000 weighin |
| `C098` | Cattle Dataset | 6,570 | 不确定 / 不确定 | 许可待核 · 需重标 · 非牛混入 | Instance Segmentation；6570 grayscale images；Multiple sourc |
| `C101` | MoDES Dataset of Cattle | 400,000 | 不确定 / 不确定 | 许可待核 · 需重标 | Monocular Depth Estimation, Segmentation；each containing 4 |
| `C111` | New Zealand Cattle Detection | 655 | 航拍高空 / 户外草场 | 许可待核 · 需重标 | 655 images, 29803 total cows；Point annotation of each visi |
| `C119` | CoBRA_pose_behaviour_youngstock | 500 | 不确定 / 室内牛舍 | 许可待核 · 需重标 | >500 images；Keypoint coordinates of annotated skeletons；Co |
| `C121` | Dataset for "Computer Vision for Resource Optimisation in Dair | 1,140 | 不确定 / 不确定 | 许可待核 · 非牛混入 · 框语义待核 | Cattle: 1140 images；YOLO...(Cow Heads, Cow Bodies, Water T |
| `C124` | M-Vet Livestock Dataset | 18,000 | 不确定 / 不确定 | 许可待核 · 需重标 · 非牛混入 | Image Classification；~18,000 images；cows, goats, pigs |
| `C128` | Counting cattle Dataset: Supporting livestock Multi Object Tra | 478 | 不确定 / 户外草场 | 许可待核 · 帧冗余 · 框语义待核 | Object Tracking, Detection, Counting；Not specified (videos |
| `C132` | RecBov51c | 27,849 | 多视角 / 不确定 | 许可待核 · 需重标 | Image Classification；27,849 images；images of back, profile |

---

## 5. P2 · 信息不足待核（36 条）

> 附表描述含糊或字段缺失，**无法在桌面阶段判定**。这些条目需要回查原始数据集页面（规模、框语义、牛体可见性）才能定级。**不建议直接放弃**——它们中可能藏着 P0/P1。

| id | 数据集 | 图像数 | 视角 / 环境 | 风险 | 缺什么信息 |
|---|---|---:|---|---|---|
| `C009` | UAV Cattle Pasture Datasets (Shao et al., 2020) | — | 航拍高空 / 户外草场 | 许可待核 | Dataset 1: 212 individual cattle targets; Dataset 2: 6 ind |
| `C014` | 3D body model dataset for Aberdeen-Angus cattle (Ruchay et al. | — | 多视角 / 室内牛舍 | 许可待核 · 需重标 · 框语义待核 | Raw RGB images and depth maps, restored point clouds; phen |
| `C025` | cow behavior dataset (Bartels et al., 2022) | — | 不确定 / 半开放牛场 | 许可待核 · 需重标 | Tri-axis accelerometer data, Labeled video footage; 197 mi |
| `C027` | COWDepth2023 (Sharma et al., 2024) | — | 顶部俯视 / 室内牛舍 | 许可待核 · 需重标 · 框语义待核 | Approximately 50 GB; Segmented raw depth/RGB pairs for ind |
| `C028` | CowDatabase3 (Ruchay et al., 2025) | — | 不确定 / 半开放牛场 | 许可待核 · 需重标 | RGB-D images, depth maps, point clouds; Key points on 3D m |
| `C029` | Aberdeen Angus Cattle Morphological Trait Dataset | — | 不确定 / 半开放牛场 | 许可待核 · 需重标 · 同源待核 | Key points on 3D models for linear morphological features; |
| `C032` | Cattle Herd Satellite Imagery Dataset (Efunogbon et al., 2025) | 260 | 航拍高空 / 户外草场 | 许可待核 · 框语义待核 · 规模偏小 | 260 high-resolution satellite images; manually annotated r |
| `C035` | Cow mounting behaviour detection dataset (Li et al., 2024a) | 9,392 | 高位斜俯视 / 户外草场 | 许可待核 · 框语义待核 · 帧冗余 | 9392 images; Manually annotated cow mounting behavior area |
| `C037` | Custom Aerial Cow Dataset (Adam et al., 2025) | 270 | 航拍高空 / 户外草场 | 许可待核 · 规模偏小 | 270 high-resolution aerial images; Manually annotated usin |
| `C040` | Japanese Black Beef Cow Behavior Classification Dataset (Shebi | — | 不确定 / 半开放牛场 | 许可待核 · 需重标 | Triaxial accelerometer sensor data, 4K video camera record |
| `C044` | Cattle Body Measurement Dataset (Y. Wang et al., 2024) | — | 不确定 / 半开放牛场 | 许可待核 · 需重标 | 275 individual cattle point clouds; Six body measurements  |
| `C046` | Multi-species Livestock 3D Morphometry Collection (Lu et al.,  | — | 地面侧视 / 室内牛舍 | 许可待核 · 需重标 · 非牛混入 | RGBD images, restored point clouds; Data from 245 animals; |
| `C050` | Livestock body condition score datasets (Zhang et al., 2023) | — | 多视角 / 实验受控 | 许可待核 · 规模偏小 · 非牛混入 · 框语义待核 | Depth images from 203 dairy cows, 201 pigs, 103 beef cattl |
| `C059` | CowDatabase (Ruchay et al., 2020) | — | 不确定 / 室内牛舍 | 许可待核 · 框语义待核 | restored point clouds; manual measurements in centimeters |
| `C068` | Annotated thermal livestock dataset (Barrios et al., 2024) | — | 航拍高空 / 户外草场 | 许可待核 · 需重标 · 框语义待核 | Not explicitly quantified; thermal images from videos |
| `C080` | Lumpy Skin Disease in dairy cows dataset (Saha, 2024) | 840 | 不确定 / 不确定 | 许可待核 · 框语义待核 | 840 RGB images (513 healthy, 327 affected); binary class |
| `C090` | Livestock 3D Body Condition Assessment Dataset (Zhang et al.,  | — | 多视角 / 实验受控 | 许可待核 · 规模偏小 · 非牛混入 · 框语义待核 | 203 dairy cows, 201 pigs, 103 beef cattle; keypoints |
| `C093` | JXcow-Datasets | — | 不确定 / 不确定 | 许可待核 · 框语义待核 · 需重标 | Semantic Segmentation；size: 112 Animals, Weight range 400– |
| `C094` | Cattle diseases datasets | — | 不确定 / 不确定 | 许可待核 · 框语义待核 | Image Classification, Detection；size: Hundreds to thousand |
| `C103` | Indian Cattle Breeds | — | 不确定 / 不确定 | 许可待核 · 框语义待核 | Image Classification；size: Not specified (images/informati |
| `C104` | Wildlife Aerial Imagery Dataset | — | 航拍高空 / 户外草场 | 许可待核 · 框语义待核 · 非牛混入 | Wildlife Detection, Classification；Not specified (10 disti |
| `C106` | Cattle Body Condition Score | — | 不确定 / 实验受控 | 许可待核 · 帧冗余 · 框语义待核 | Body Condition Scoring；Not specified (collection of precla |
| `C107` | Dairy Cow Drinking/Brushing Behavior Video Event Dataset and c | — | 不确定 / 室内牛舍 | 许可待核 · 帧冗余 · 框语义待核 | Behavior Analysis；Video clips；Per-cow event annotation tab |
| `C110` | Direct measurement of dairy cow body condition using a 3D came | — | 地面侧视 / 实验受控 | 许可待核 · 框语义待核 | Body Condition Scoring；3D frames, Color images；Not specifi |
| `C112` | Labeled RGB and depth images for cattle body condition score p | — | 不确定 / 实验受控 | 许可待核 · 帧冗余 · 框语义待核 | Body Condition Score Prediction；Not specified；Labeled acco |
| `C113` | Computer Vision Dataset for Detecting Cattle Behaviors in Past | — | 不确定 / 户外草场 | 许可待核 · 框语义待核 | YOLOv8-format annotation files for behaviors；Bounding box  |
| `C115` | Image dataset for cow identification, including code to train  | — | 不确定 / 不确定 | 许可待核 · 框语义待核 | Cow Identification；size: Not specified；annot: Not specifie |
| `C116` | Sample Data and Annotations for "Beyond Proximity: Pose-Based  | — | 顶部俯视 / 室内牛舍 | 许可待核 · 帧冗余 · 框语义待核 | Cow bounding box annotations, Anatomical keypoint annotati |
| `C117` | CoBRA_segmentation_youngstock | 250 | 不确定 / 室内牛舍 | 许可待核 · 需重标 · 规模偏小 · 框语义待核 | Segmentation, Behavior Classification；250 segmented images |
| `C118` | CoBRA_re_identification_youngstock | — | 不确定 / 室内牛舍 | 许可待核 · 框语义待核 | Re-identification；11,438 animal segments（非图像数） |
| `C120` | CoBRA_pose_behaviour_youngstock_video | — | 不确定 / 室内牛舍 | 许可待核 · 帧冗余 · 框语义待核 | Videos (.mp4)；100 videos of 60s (2fps) |
| `C126` | Edge AI for Precision Livestock Farming: KPI Dataset from a Vi | — | 不确定 / 户外草场 | 许可待核 · 框语义待核 | System Performance Evaluation；modality: Not specified；anno |
| `C127` | Cattle side view and back view dataset | — | 多视角 / 不确定 | 许可待核 · 规模偏小 · 框语义待核 | size: 72 cattle；Images (side and back views) |
| `C130` | Animal Action Video Dataset with Heatmap and Silhouette Repres | — | 不确定 / 不确定 | 许可待核 · 框语义待核 · 非牛混入 | Action Recognition, Video Classification；25 distinct anima |
| `C131` | Cattle image datasets for lameness detection and analysis | 277 | 不确定 / 半开放牛场 | 许可待核 · 规模偏小 · 框语义待核 | Lameness Detection and Analysis；size: 277 images |
| `C133` | A comprehensive image dataset of Bangladeshi cow breed identif | 263 | 不确定 / 不确定 | 许可待核 · 规模偏小 | Breed Identification；size: 263 HD image data |

---

## 6. X · 不兼容（56 条）

> 按不兼容原因分组。**注意：X 不代表数据无价值**——其中相当一部分可用于 CowCV 的**非检测任务视图**（关键点、行为、体况评分等），只是不能进当前的单类整牛 HBB 检测基准。

### 6.1 无检测框语义（纯分类/回归/传感器/音频）（23 条）

| id | 数据集 | 图像数 | 视角 / 环境 | 风险 | 判断依据 |
|---|---|---:|---|---|---|
| `C002` | Cattle Retinal Fundus Image dataset (Cihan et al., 2024) | 1,118 | 不确定 / 实验受控 | 许可待核 | RGB retinal fundus images; Expert veterinarian labels as C |
| `C007` | CattNISDB dataset (Saygılı et al., 2024) | 2,430 | 不确定 / 实验受控 | 许可待核 | Retinal fundus images (color digital); Images tied to anim |
| `C018` | Pasture Parameter Estimation Dataset (Defalque et al., 2024) | — | 不确定 / 户外草场 | 许可待核 | Multispectral band signals, Vegetation indices, Meteorolog |
| `C022` | Meat Freshness Image Dataset (Büyükarıkan, 2024) | 2,266 | 不确定 / 不确定 | 许可待核 | Objective Detection of Beef Quality; Implicitly annotated  |
| `C023` | cattle retinal fundus images dataset (Cihan et al., 2025) | 1,110 | 不确定 / 不确定 | 许可待核 · 同源待核 | 1110 good quality retinal images (selected from 2430, from |
| `C061` | FriesianCattle2015 dataset (Andrew et al., 2016) | 764 | 顶部俯视 / 室内牛舍 | 许可待核 | 764 RGB-D image pairs; Individual identities for compariso |
| `C063` | Dairy Cow Behavior Dataset (Pongsanun et al., 2025) | — | 不确定 / 室内牛舍 | 许可待核 | Time-series sensor data (accel + gyro); 784,530 observatio |
| `C065` | Cattle Behavior Classification dataset (Li et al., 2021) | — | 不确定 / 不确定 | 许可待核 | Inertial sensor time-series data; 530,485 rows from 6 cows |
| `C069` | MeatScan dataset (Gyening et al., 2025) | 11,000 | 不确定 / 不确定 | 许可待核 | Binary Classification fresh/spoiled meat; 11,000 RGB image |
| `C070` | RuuviTag Calf Activity Dataset (Ouannes et al., 2025) | — | 不确定 / 室内牛舍 | 许可待核 | Triaxial acceleration data; 90,720,000 raw readings |
| `C071` | CowTeatVideo Benchmark (Zhang et al., 2022) | — | 不确定 / 室内牛舍 | 许可待核 · 框语义待核 | Teat-end Hyperkeratosis Assessment; ~21,191 frames/video |
| `C078` | CowScreeningDB (Ismail et al., 2023) | — | 不确定 / 室内牛舍 | 许可待核 | Raw IMU data (accelerometer, gyroscope); 11,518 samples |
| `C079` | B-mode Mammary Gland Sonogram Dataset with Echotexture Feature | 3,072 | 不确定 / 不确定 | 许可待核 | B-mode sonograms (images), echotexture analysis variables |
| `C081` | Dairy Cow Hypocalcaemia Prediction Dataset (Leerdam et al., 20 | — | 不确定 / 不确定 | 许可待核 | Behavioral sensor data (5 features daily over 21 days) |
| `C082` | Dairy Cattle Shade-Seeking Behavior Dataset (Sanjuan et al., 2 | — | 不确定 / 半开放牛场 | 许可待核 | Numerical records (camera-derived counts); 6907 observatio |
| `C084` | Dairy Cow Grazing Time Dataset (Guyard & Delagarde, 2025) | — | 不确定 / 不确定 | 许可待核 | Accelerometer readings; 1224 cow x day datapoints |
| `C097` | Cattle bioacoustic dataset | — | 不确定 / 户外草场 | 许可待核 | modality: Bioacoustic data (audio) |
| `C105` | CATTLE ESTRUS DETECTION PATCH IMAGES | — | 不确定 / 不确定 | 许可待核 · 框语义待核 | CATTLE ESTRUS DETECTION PATCH IMAGES；Manually altered to s |
| `C108` | Quantification of grass-severing bites performed by grazing ca | — | 不确定 / 户外草场 | 许可待核 | modality: Accelerometer data |
| `C122` | Infrared thermal images and corresponding pH, temperature, and | 60 | 不确定 / 实验受控 | 许可待核 · 规模偏小 | Infrared Thermal Images；60 bovine half-carcasses |
| `C123` | Accelerometer-Based Multivariate Time-Series Dataset for Calf  | — | 不确定 / 不确定 | 许可待核 | modality: Accelerometer Data；27.4 hours of accelerometer d |
| `C125` | IoT sensor data XGain UC6 | — | 不确定 / 户外草场 | 许可待核 · 同源待核 | modality: Accelerometer Data；sensor data from 10 cows over |
| `C134` | Study on Grassland Dynamics and Livestock Behavior Changes Und | — | 不确定 / 户外草场 | 许可待核 | modality: GPS Data, Remote Sensing Imagery；NDVI data |
### 6.2 局部特写/部位框（牛体不在画面内）（19 条）

| id | 数据集 | 图像数 | 视角 / 环境 | 风险 | 判断依据 |
|---|---|---:|---|---|---|
| `C001` | Simmental beef cattle face dataset (Li et al., 2022c) | 10,239 | 不确定 / 户外草场 | 许可待核 | Cropped RGB face images; YOLOv3 ... automatic face detecti |
| `C004` | Cattle muzzle biometric dataset (Shojaeipour et al., 2021) | 2,900 | 不确定 / 户外草场 | 许可待核 | RGB images of animal faces (muzzle patterns); individual i |
| `C008` | Beef Cattle Muzzle Image Dataset (Li et al., 2022a). | 4,923 | 不确定 / 半开放牛场 | 许可待核 | Manually cropped RGB muzzle images; Individual cattle ID l |
| `C015` | Cattle Muzzle Pattern Dataset 300 (Pathak & Prakash, 2025) | 2,900 | 不确定 / 实验受控 | 许可待核 | Photographic (face and muzzle features); cattle heads fixe |
| `C016` | CMPD268 (Pathak & Prakash, 2025) | 4,923 | 不确定 / 不确定 | 许可待核 · 同源待核 | Muzzle images; Manually cropped to isolate the muzzle area |
| `C017` | CMPD568 (Pathak & Prakash, 2025) | — | 不确定 / 不确定 | 许可待核 · 框语义待核 · 同源待核 | Mixed photographic (face and muzzle); Combined size of CMP |
| `C030` | Cattle Face Recognition Dataset (Ruchay et al., 2024) | 315 | 不确定 / 室内牛舍 | 许可待核 · 规模偏小 | 315 raw RGB images of 91 Aberdeen Angus cattle; face detec |
| `C039` | Cattle Face Recognition Dataset (Xiao et al., 2025) | 14,047 | 不确定 / 半开放牛场 | 许可待核 | Cropped cattle face images; XML files with bounding box co |
| `C043` | Cattle Identification Dataset (Roy & Raman, 2025) | 5,224 | 不确定 / 不确定 | 许可待核 | modality: Images (muzzle and face of cattle); task: Animal |
| `C045` | Cattle Muzzle Image Dataset (Kimani et al., 2023) | 4,923 | 不确定 / 户外草场 | 许可待核 · 同源待核 | modality: Muzzle images (resized to 300x300 pixels); 4923  |
| `C049` | Cattle Biometrics Dataset (Ahmed et al., 2024) | 2,893 | 不确定 / 不确定 | 许可待核 | bounding boxes around muzzles labeled "muzzle" |
| `C060` | CattleEyeView dataset height (Ong et al., 2023) | 30,703 | 顶部俯视 / 户外草场 | 许可待核 · 实例密度低 · 帧冗余 | 753 cow instances in 30,703 frames; body+head boxes |
| `C062` | Cow Nose Image Pattern Database (Bello et al., 2020) | 4,000 | 不确定 / 不确定 | 许可待核 | High-resolution images of cow noses; converted to grayscal |
| `C067` | Holstein2025 dataset (Shu et al., 2025) | 3,915 | 不确定 / 室内牛舍 | 许可待核 | 3915 individual cow face images; cropped face images |
| `C072` | Cow Ear Tag Detection Dataset and Cow Ear Tag Recognition Data | 2,675 | 不确定 / 不确定 | 许可待核 | TXT-format label files for ear tag regions using Labelimg |
| `C099` | Cattle Body Parts Dataset for Object Detection | 428 | 不确定 / 不确定 | 许可待核 · 同源待核 | annot: Bounding boxes for "Back," "Head," and "Leg" |
| `C100` | Cow Muzzle Dataset | — | 不确定 / 不确定 | 许可待核 | Cow Identification, Muzzle Detection；YOLO-format label fil |
| `C114` | Cows Frontal Face Dataset | — | 不确定 / 不确定 | 许可待核 | Cow Identification, Muzzle Detection；limited to muzzle det |
| `C129` | Annotated Cattle Images dataset | 6,182 | 不确定 / 开放网络混合 | 许可待核 | 6182 cattle images；Animal face localization, Main facial s |
### 6.3 有整牛框但被其他条件否决（规模/同源）（7 条）

| id | 数据集 | 图像数 | 视角 / 环境 | 风险 | 判断依据 |
|---|---|---:|---|---|---|
| `C012` | Aerial Livestock Dataset (Han et al., 2019) | 89 | 航拍高空 / 户外草场 | 许可待核 · 规模偏小 · 非牛混入 | 4996 annotated livestock instances across 89 high-resoluti |
| `C056` | OpenCows2020 dataset (Andrew et al., 2021) | 3,707 | 顶部俯视 / 室内牛舍 | 许可待核 | 3,707 whole images (detection), 4,736 cropped torso region |
| `C058` | FriesianCattle2017 dataset (Andrew et al., 2017) | 940 | 顶部俯视 / 室内牛舍 | 许可待核 | 940 top-down stills from 89 Holstein Friesian cows |
| `C075` | COw LOcalization dataset (Das et al., 2025) | 1,254 | 不确定 / 室内牛舍 | 许可待核 | 1,254 images, 11,818 cow instances; YOLO format boxes |
| `C086` | CBVD-5 (Li et al., 2024c) | 206,100 | 不确定 / 室内牛舍 | 帧冗余 · 标注质量不达标 · 许可待核 | 4122 keyframes with detection boxes; 206,100 image samples |
| `C096` | Animals Detection Images Dataset | — | 不确定 / 开放网络混合 | 许可待核 · 同源待核 · 非牛混入 | env: Not specified (Google Open Images V6+)；classes like D |
| `C102` | Open Images V7 Animals YOLO | — | 不确定 / 开放网络混合 | 许可待核 · 同源待核 · 非牛混入 · 框语义待核 | Object Detection；env: Not specified (subset of Open Images |
### 6.4 仅掩膜或关键点，且牛体可见性未明（6 条）

| id | 数据集 | 图像数 | 视角 / 环境 | 风险 | 判断依据 |
|---|---|---:|---|---|---|
| `C013` | Beef Cattle PCD Dataset (Hou et al., 2023) | — | 不确定 / 室内牛舍 | 许可待核 | 3D surface point clouds; Semantic-segmentation-editor tool |
| `C019` | Cattle Rib-Eye Ultrasound Dataset (Melo et al., 2022) | 67 | 不确定 / 不确定 | 许可待核 · 规模偏小 · 需重标 | 67 gray-scale ultrasound images; rib-eye area delineated b |
| `C021` | AI Hub dataset (Lim & Song, 2025) | 77,899 | 不确定 / 不确定 | 许可待核 | RGB images, Segmentation masks; beef carcass cross-section |
| `C034` | Image dataset for cattle biometric detection and analysis (Bai | 144 | 多视角 / 户外草场 | 许可待核 · 规模偏小 · 需重标 | 144 images (72 back views, 72 side views); four key measur |
| `C041` | CattleFace-RGBT dataset (Coffman et al., 2024) | 4,600 | 不确定 / 实验受控 | 许可待核 | RGB and thermal facial image pairs; 13 key points ... (eye |
| `C085` | NWAFU-Cattle dataset (Fan et al., 2023) | 2,432 | 多视角 / 不确定 | 许可待核 · 非牛混入 | 16 keypoints on cattle instances, following COCO format |
### 6.5 旋转框（理论上可转，但被其他条件否决）（1 条）

| id | 数据集 | 图像数 | 视角 / 环境 | 风险 | 判断依据 |
|---|---|---:|---|---|---|
| `C057` | Cows2021 dataset (Gao et al., 2021) | 10,402 | 顶部俯视 / 室内牛舍 | 许可待核 | 10,402 still RGB images; Oriented bounding-box annotations |

---

## 7. 域标签分析：CowCV 的覆盖缺口

打标时同步标注了 CowCV 的域维度（视角 / 环境 / 光照）。分布如下：

| 视角 | 条数 | | 环境 | 条数 | | 光照 | 条数 |
|---|---:|---|---|---:|---|---|---:|
| 不确定 | 85 | | 不确定 | 40 | | 不确定 | 82 |
| 多视角 | 11 | | 室内牛舍 | 32 | | 白天RGB | 25 |
| 航拍高空 | 10 | | 户外草场 | 27 | | 混合 | 14 |
| 顶部俯视 | 10 | | 半开放牛场 | 20 | | 人工照明 | 10 |
| 地面侧视 | 9 | | 实验受控 | 12 | | 红外 | 2 |
| 高位斜俯视 | 9 | | 开放网络混合 | 3 | | 低照度 | 1 |

**两点值得注意**：

1. **63% 的条目视角无法判定**（85/134）——附表 `Imaging environment` 字段普遍只写地点、不写机位，这是原综述的元数据短板，也是 CowCV 域标签体系「元数据缺失」论点的又一实证。
2. **「航拍高空」有 10 条**——这正是《CowCV 候选数据集评估（边界框类）》附录 B 指出**缺失**的域档。若从 P0/P1 中筛出航拍类，可直接填补该缺口。
3. **红外仅 2 条**——与 Bhujel 2025「热成像/红外极少」的结论一致，对 CMBN、HCRD 等红外数据参与的跨域实验仍是稀缺资源。

---

## 8. 与 CowCV 已纳入 14 项的同源情况

初筛中标记 `同源待核` 的共 **11 条**：

| id | 数据集 | 疑似同源对象 |
|---|---|---|
| `C016` | CMPD268 (Pathak & Prakash, 2025) | 吻部裁剪特写；4923张与C008/C045疑似同源 |
| `C017` | CMPD568 (Pathak & Prakash, 2025) | 面部/吻部特写合集，牛体不在画面内；为C015+C016合并 |
| `C023` | cattle retinal fundus images dataset (Cihan et al., 2025) | 视网膜图像；与C007同URL同批次2430，疑似重复 |
| `C029` | Aberdeen Angus Cattle Morphological Trait Dataset | 字段与C028完全相同，疑似重复；牛体可见性及图像数待核 |
| `C045` | Cattle Muzzle Image Dataset (Kimani et al., 2023) | 鼻纹(muzzle)特写，牛体不在画面内；4923张与C008/C016疑似同源 |
| `C051` | Cattle Pose Estimation Dataset (Li et al., 2019) | 仅有16关键点需补整牛HBB；同属NWAFU，是否与已纳入NWAFU同源待核 |
| `C074` | MultiCamCows2024 (Yu et al., 2025) | 仅躯干裁剪＋COCO检测框，范围待核；挤奶后多相机，或与Cows2021同组 |
| `C096` | Animals Detection Images Dataset | Open Images V6+ 派生，与已纳入 Google Open Images cow subset 疑同源 |
| `C099` | Cattle Body Parts Dataset for Object Detection | 部位框非整牛；可能与已纳入 CBPD_ODD 同源 |
| `C102` | Open Images V7 Animals YOLO | Open Images 派生，与已纳入 cow subset 疑同源；规模未定 |
| `C125` | IoT sensor data XGain UC6 | 纯传感器；且与已纳入 XGain 同源 |

> 已可确认的同源与既有决策（无需再查）：
> - **C086 `CBVD-5`** → CowCV 文档 §3.1 已因其漏标严重明确**暂缓**（见附录 B ④）
> - **C085 `NWAFU-Cattle dataset`** → 已在 CowCV 14 项清单中（NWAFU Cattle Dataset），且 URL 指向 CMBN
> - **C075 `COw LOcalization dataset`** → 即已纳入的 COLO
> - **C096 / C102** → Google Open Images V6+/V7 派生，与已纳入的 cow subset 疑同源
> - **C105 `CattleEyeView`** → 已在早期评估中排除（场景冗余 + 标注混杂）

---

## 9. 下一步建议

按性价比排序：

1. **先做 P0 的 12 条网页核验**（许可 + 可达性 + 样本抽检）。工作量小，收益最直接。
2. **P2 的 36 条做一次批量回查**——只查两件事：图像数、框语义。查完可大批转入 P0/P1。
3. **航拍档专项**：把 P0/P1 中的航拍类挑出来，评估是否新增「无人机高空航拍」域标签档。
4. **P1 的重标成本评估**：38 条需重标，其中仓库存量类数据（参考 P2 规模）价值最高，值得优先补框。
5. **许可先于一切**：134 条全带 `许可待核`。CowCV 要发布数据门户，建议在收集阶段就同步记录许可证字段，避免后期返工。

---

## 附录 A. 完整 134 条标签表

见同目录 CSV：`cowcv_ruchay2026_screening.csv`（UTF-8 BOM，Excel 可直接打开）。

字段：`id, sheet, grade, name, task, modality, env, size, annot, apps, view, scene, illum, box_semantics, img_count, risks, confidence, evidence, note, url, year, span`

---

## 附录 B. 数据修正记录

原附表存在两类质量问题，本表使用的是**修正后**数据：

**① 列内容互换（41 行）**
`mmc3.xlsx` 的 `Beef` / `Dairy` 两 sheet 中，自某行起 `B 列(AI Task Category)` 与 `D 列(Imaging environment)` 的内容被整列互换——B 列装的是采集环境（如 "Open-pen setting"、"Feedlot in the Kostroma region, Russia"），D 列装的是任务类别（如 "Behavioral Analysis"）。
- 修正方法：对称判据——比较「交换前」与「交换后」两列的语义得分，交换后显著更合理（差值 ≥2）才交换
- 修正行数：Beef 27 行 + Dairy 14 行 = **41 行**
- 注：`mmc4.xlsx` 的 `Cattle` sheet **无此问题**

**② 合并单元格导致的假缺失**
`mmc3.xlsx` 存在跨行合并（Beef 42 个、Dairy 76 个、Cattle 0 个）。A 列合并表示**一个数据集占多行**，B–G 列共享值，而 **H 列（Web Link）逐行独立**，承载多条链接（主数据 / 源码 / Dataset1-3）。
- 未处理时：12 条 `env`、9 条 `size` 显示为缺失
- 处理后：**所有字段缺失归零**，另发现 **7 条含多个下载链接**

**③ 条数口径**
以 A 列（数据集名）非空行为准 → **134 条**（Beef 46 + Dairy 45 + Cattle 43）。若把合并的从属行也展开会得到 154 条，那是**错误口径**。

**④ 打标规范的两处遗漏（在合并阶段人工修正）**

- **CBVD-5 未被写进规范**：CowCV 文档 §3.1 已明确"CBVD-5 现有标注存在较大范围的漏标和不完整标注，暂不纳入"。初筛规范漏了这条**既有决策**，导致 C086 被误判为 P0。已在合并阶段修正为 `X`，并补 `标注质量不达标` 风险标签。
- **`帧冗余` 未与等级联动**：连续视频帧冗余不构成不兼容（分层抽样即可解决），但会实质影响"能否直接纳入"的判断。保留原等级，改为在 P0 节单列提示。

---

## 附录 C. 证据与推断的边界

- **事实**：`name` / `task` / `modality` / `env` / `size` / `annot` / `apps` / `url` 均为附表原文（已修正列互换与合并问题）
- **推断**：`grade` / `box_semantics` / `img_count` / `view` / `scene` / `illum` / `risks` 均为基于附表文字的判断，**未经网页或数据核验**
- **待核**：全部 134 条的**许可**；36 条 P2 的规模与框语义；11 条同源关系
- 每条判断的 `evidence` 字段保留了所引附表原文，`confidence` 给出了置信度（high 54 / medium 53 / low 27）

---

*生成于 2026-09-28 · 数据源：Ruchay et al. 2026 补充材料 Annex 3/4 · 打标规范：CowCV 检测视图硬约束（文章初稿 §2.2/§3.1/§3.2/§3.3）*
