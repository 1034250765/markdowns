---
id: cattle27-public-dataset-evidence
type: source
status: draft
created: 2026-10-13
updated: 2026-10-13
sources:
  - 牛只数据集/134个数据集信息收集/27个牛类公开数据集详细档案.md
  - 牛只数据集/134个数据集信息收集/精准畜牧养殖公开计算机视觉数据集系统综述 (Comput Electron Agric 2025).md
  - 牛只数据集/134个数据集信息收集/开放数据集与AI-GenAI驱动的精准畜牧计算机视觉双向综述 (Comput Electron Agric 2026).md
  - 牛只数据集/134个数据集信息收集/CowCV 候选数据集评估（边界框类）.md
  - 牛只数据集/拍摄环境与场景.md
  - 牛只数据集/数据集融合方法Fusion or Confusion (CVPR 2025 Workshop).md
  - https://arxiv.org/abs/2406.10628v1
  - https://github.com/Anil-Bhujel/Public-Computer-Vision-Dataset-A-Systematic-Survey
  - https://data.bris.ac.uk/datasets/wurzq71kfm561ljahbwjhx9n3/readme.txt
  - https://data.bris.ac.uk/data/dataset/10m32xl88x2b61zlkkgz3fml17
  - https://github.com/Wormgit/Cows2021
  - https://zenodo.org/records/6324361
  - https://zenodo.org/records/10535934
  - https://zenodo.org/records/3981400
  - https://github.com/ruchaya/CowDB
  - https://github.com/ruchaya/CowDatabase
  - https://github.com/ruchaya/CowDatabase2
  - https://github.com/AnimalEyeQ/CattleEyeView
  - https://raw.githubusercontent.com/Jiahao-Ma/MultiviewC/main/README.md
  - https://vhasoares.github.io/downloads.html
  - https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0269259
  - https://arxiv.org/abs/2305.16555
  - https://docs.ultralytics.com/datasets/detect/
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html
  - https://help.zenodo.org/docs/deposit/about-records/
  - https://creativecommons.org/licenses/by-nc-nd/4.0/
  - https://www.ifm.com/gb/en/product/O3D303
  - https://openaccess.thecvf.com/content/CVPR2025W/PBVS/html/Becker_Fusion_or_Confusion_A_Look_at_Dataset_Pooling_for_Infrared_CVPRW_2025_paper.html
---

# 牛类公开数据集 27 条档案：版本、标注与获取核查

## 资料与产物

主资料为 [2026-09-28 的 27 条历史档案](牛只数据集/134个数据集信息收集/27个牛类公开数据集详细档案.md)，本次核查日期为 2026-10-13。按用户要求形成 [科研记录](../../科研记录/27个牛类公开数据集详细档案.md)，包含 27 条卡片、10 张表、两幅 Study Image 概念图和一幅精确计数图；[文字底稿](../../科研记录/27个牛类公开数据集详细档案.assets/表格可编辑底稿.md)与[结构化数据](../../科研记录/27个牛类公开数据集详细档案.assets/档案与图表数据.json)保留展示图中的全部数字。

本页用于发现来源和冲突；逐条 DOI、获取入口、许可状态、读取范围与操作步骤以科研记录及原资料为准。科研记录的格式参考和既有排版参照不计入本页的 28 个研究来源。

## 核心事实及定位

- **版本事实：** 27 为主档案对 Bhujel 预印本牛类条目的整理；预印本跨物种范围为 58。正式版扩展统计沿用本地综述笔记，未在本次获取正式版全文重算。参见科研记录 §2.1、L1/L2、O1/O2。
- **发布事实：** FriesianCattle2015 官方 README 列 83 张训练图与 294 张测试图；其 377 张发布划分数量与综述 764 对 RGB-D / 92 头分开记。参见卡片 A1、O3。
- **仓库事实：** CowDB、CowDatabase、CowDatabase2 的作者仓库分别记 154、103、119 头；最后一项与本地笔记的 96 头分析口径保留差异。三资源是否有成员重叠未证明。参见卡片 C3–C5、O9–O11。
- **发行事实：** CowBehavior Zenodo 记 253 视频 / 1,526,473 标注帧，论文用 280 视频；27 段含人物视频从公开发行删去而保留 JSON。参见卡片 D1、O8。
- **任务事实：** Cows Frontal Face v2 当前说明限定鼻纹检测，459 类不能作为已完成身份识别实验的证据。参见 B4、O7。
- **计数事实：** CattleEyeView 的 753 不同实例与 30,703 帧不能直接推算每帧密度。作者仓库通过表单提供数据申请入口，代码公开可读不等于数据已下载。参见 E6、O12。
- **模态事实：** Dairy Cow 原论文写红外模式监控，不足以确认测温热成像；MultiviewC 的三维标注与标定不自动证明存在深度图；ifm O3D303 厂商标为 ToF camera。参见 D4/D5/E5、O13/O15/O21。

## 综合与推断边界

本次方法综合认为：标签表示统一后仍需核对整牛、躯干、头部和鼻纹语义；多帧、多视角与增强样本需按研究问题建立来源组；获取、格式、标注质量、独立性和许可应分别验收。科研记录 §4 给出尚待执行的 SOP，不作为原包审计完成证据。

[既有边界框候选评估](<../../牛只数据集/CowCV 候选数据集评估（边界框类）.md>) 中的 Bristol 同源判断是风险线索，缺少图片 / 成员审计时不升级为已证明泄漏。CattleEyeView 的低密度推断不成立；历史排除决定保留，但新记录提出条件性复议，不直接变更 CowCV 成员。航拍场景相似不证明近重复，Cattle-counting 的多因素采集不证明严格正交。

[Fusion or Confusion 的本地笔记](<../../牛只数据集/数据集融合方法Fusion or Confusion (CVPR 2025 Workshop).md>)与原论文用于提出单源 / 同域池 / 跨域池的实验设计线索；车辆研究的收益不作为牛只池化的结果。

## 未核实与相关记录

Dataverse 本次正文受反机器人限制；Kaggle 404、Aerial Pasture 原站失效与镜像情况仍为历史记录。全部压缩包、文件级数量、许可文本、逐图标签、重复成员、实际分组和模型性能未逐一核查。数据库与向量索引同步未运行。

原始资料未改写。[补充核查记录](../../科研记录/27个牛类公开数据集详细档案.assets/补充来源核查.json)和[来源 hash](../../科研记录/27个牛类公开数据集详细档案.assets/本地来源校验.json)保留本次读取证据；后续数据准备参见 [既有独立测试评估来源摘要](cowcv-dataset-test-evaluation-evidence.md)。
