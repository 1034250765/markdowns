---
id: cowcv-capture-environment-scene-evidence
type: source
status: draft
created: 2026-10-13
updated: 2026-10-13
sources:
  - 牛只数据集/拍摄环境与场景.md
  - 牛只数据集/COLO.md
  - 牛只数据集/7月工作.md
  - 牛只数据集/域内重测-10月.md
  - 牛只数据集/10月域内重测计划.md
  - 牛只数据集/27个牛类公开数据集详细档案.md
  - 科研记录/实验记录格式参考.md
  - 科研记录/数据集整理与独立测试集评估.md
  - https://arxiv.org/html/2105.01938
  - https://arxiv.org/html/2503.13777
  - https://arxiv.org/html/2407.20372
  - https://openaccess.thecvf.com/content/WACV2026/html/Christiansen_MooTrack360_A_Novel_Fisheye_Camera_Dataset_for_Robust_Multi_Diary_WACV_2026_paper.html
  - https://zenodo.org/records/15688349
  - https://github.com/ameybhole/IIHC
  - https://github.com/bhuiyanmobasshir94/CID
  - https://github.com/MicaleLee/Database
  - https://arxiv.org/abs/1405.0312
  - https://storage.googleapis.com/openimages/web/index.html
  - https://arxiv.org/abs/1803.09010
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html
  - https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html
  - https://docs.ultralytics.com/modes/val/
  - https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py
---

# 牛只测试数据拍摄环境与场景：采集条件及来源核查

## 资料范围与用途

本页对应[用于测试的数据集拍摄环境与场景](../../科研记录/用于测试的数据集拍摄环境与场景.md)，整理指定场景档案、相关本地记录与原始研究／官方指南。完整场景表、过程记录、方案与来源编号见科研记录附录 A。

本次核查日期为 2026-10-13。只完成文件与来源核查、场景综合和图表制作，未对原始图像包逐图审核，未连接远程服务器、抽帧、采集或重跑检测评估。原始资源数量、项目历史视图与 10 月 test 数量分别记录。

## 来源明确记载的事实

- [场景档案](../../牛只数据集/拍摄环境与场景.md)§4.3 与[COLO 笔记](../../牛只数据集/COLO.md)末段一致记录，CowCV 只含 Top+Side 的 1,004 图，不含原资源 External 的 250 图；原采集设备与机位对应论文说明。
- 场景档案 §4.6 记录 HCRD 采用 1,063 张配框 `full photo` RGB，原资源的成对热图没有纳入当前检测视图；受控侧视采集不等于已证实固定安装。
- 场景档案 §4.2、§4.7 与[7月工作](../../牛只数据集/7月工作.md)§10–11 支持 8-Calves 使用 900 静态检测帧、CID 只用 `images` 的 2,056 图并排除 `yt_images`；原跟踪规模与检测子集不可混用。
- [10 月重测](../../牛只数据集/域内重测-10月.md)§4.2 的 14 个 test 图数复算合计 3,124；本次没有远程重新计数，也未据此确认各场景比例或全部关联组隔离。
- 原始研究和官方资源支持 Cows2021 的固定俯视走道与躯干定向框、COLO 的多视角与光照资源、MooTrack360 的密集鱼眼、多相机与日夜资源，以及 COCO／Open Images 的异质开放来源。设备细节若只取得摘要或未能打开全文，保留场景档案摘录的证据限制。

## 综合分析与方案

**综合：** 14 个数据集同时承载场地、视角、镜头、光照／模态、尺度、遮挡、来源与标注差异，不能直接当作 14 个等价的环境域。网络来源与混合来源尤其需要图像级标签。

**方案：** 为每张 test 图登记路径、hash、设备／场景、时序、牛 ID、原图变体、标注语义与证据定位；按研究问题定义时间、个体、相机或场地独立性，再核对来源关联和重复。GroupShuffleSplit 只按已定义组划分，不能替研究者定义何种关联需要隔离。

**推断与待检验假设：** 视角、鱼眼边缘、目标尺度、牛间／管杆遮挡可能对应不同失败模式，但跨数据集指标不能独立证明单一因素的因果作用。记录提出分层方案，没有新增模型结果。

## 冲突与尚待确认

1. **Dairy Cow 模态及子集口径：** [综述档案](牛只数据集/134个数据集信息收集/27个牛类公开数据集详细档案.md)将相关姿态资源写为 IR、1,800 图；场景档案描述项目日夜外观与公开页约 1,980 图，7 月实际目录统计为 2,320+1,800=4,120。需要对照论文、子目录和图像成员，不能将整个组合统一写成 RGB 或 IR。
2. **Cows2021 最终框语义：** 原始躯干 OBB、水平外接框、人工复核标签与部位类别筛选的逐版本关系未核查；转换不自动证明整牛重标。
3. **设备与采样：** 8-Calves、CID、Dairy Cow、NWAFU 等设备／采集缺项保留 `unknown`；XGain 的 6 m 和相机细节来自场景档案配套文章摘录，本次未独立取得该文章全文。
4. **独立性与覆盖率：** 10 月 SHA-256 去重及 8:1:1 描述不等于视频／相机／牛级全部隔离；当前场景分布、原始图像包、split 与内容 hash 仍需成员级核查。

## 归档与复核

科研记录使用 Study Image 场景／流程图及表格母版，本地确定性排字；全部 6 张表同时保留 Markdown、JSON 和 PNG 元数据，提供空白 scene manifest 模板。源文件 hash、访问结果／核查摘要、绘图脚本与复核结果存入同名 assets。HCRD、CID 与 OpenCV 入口未取得可读正文；MooTrack360 只取得官方摘要，XGain 取得 DOI 元数据，相应详细条件保留本地摘录的证据限制。

已检查链接、表格一致性、数量复算、Frontmatter 与索引。数据库与向量索引同步未运行；原始资料和用户已有修改保留。
