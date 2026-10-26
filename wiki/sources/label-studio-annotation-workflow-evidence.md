---
id: label-studio-annotation-workflow-evidence
type: source
status: draft
created: 2026-10-13
updated: 2026-10-13
sources:
  - 服务器/Label-Studio操作指南.md
  - 牛只数据集/label studio.md
  - 服务器/71相关.md
  - 牛只数据集/7月工作.md
  - 牛只数据集/拍摄环境与场景.md
  - https://labelstud.io/guide/storage_local
  - https://labelstud.io/guide/predictions
  - https://labelstud.io/templates/image_bbox
  - https://labelstud.io/tags/rectanglelabels
  - https://labelstud.io/guide/task_format
  - https://labelstud.io/guide/labeling
  - https://labelstud.io/guide/access_tokens
  - https://api.labelstud.io/api-reference/api-reference/projects/import-tasks
  - https://labelstud.io/guide/label_studio_compare
  - https://labelstud.io/guide/signup
  - https://labelstud.io/guide/export
  - https://labelstud.io/guide/ml
  - https://labelstud.io/guide/install.html
  - https://pypi.org/project/label-studio/1.23.0/
  - https://docs.ultralytics.com/datasets/detect/
  - https://www.sqlite.org/cli.html
  - https://www.sqlite.org/backup.html
  - https://github.com/HumanSignal/label-studio/blob/1.23.0/label_studio/data_import/api.py
---

# Label Studio 标注流程：本地指南与官方文档核查

## 资料范围

本页是 2026-10-13 阅读的一组本地记录与官方资料的来源摘要。完整编号、链接和定位见[科研记录的附录 B](../../科研记录/Label-Studio进行数据标注的分析与操作步骤.md#附录-b-来源与定位references)；操作规程、试标设计与示意图见[科研记录正文](../../科研记录/Label-Studio进行数据标注的分析与操作步骤.md)。

本地资料属于个人操作与研究记录，外部资料为官方文档、包元数据、指定版本源码及 SQLite / Ultralytics 文档。持续更新的官网说明不能证明历史实例已经升级或当前仍运行。

## 事实与来源定位

- [本地操作指南](../../服务器/Label-Studio操作指南.md)§0、§10 保存了 2026-07-12 的实例快照：yxli 实例为 LS 1.23.0 / Python 3.10 / 8080，包含 60 tasks / 52 predictions 与 2056 / 2056 的项目记录。本次未连接服务器，不能确认现在的状态。
- [矩形框模板](https://labelstud.io/templates/image_bbox)和 [RectangleLabels 标签说明](https://labelstud.io/tags/rectanglelabels)支持图像水平框任务；结果左上角和宽高使用百分比，`canRotate` 可以隐藏旋转控制。
- [预标注文档](https://labelstud.io/guide/predictions)支持导入 `data` 和 `predictions`。预测只读，可以复制为 annotation 再由人修正；模型建议与人工结果应区分。
- [本地存储文档](https://labelstud.io/guide/storage_local)提供目录连接、Files / Tasks 导入和 Save / Sync 路线；`d=` 为相对 DOCUMENT_ROOT 的媒体路径。手动导入 JSON 时保存连接、避免重复扫描建任务，是一种特定流程。
- [令牌说明](https://labelstud.io/guide/access_tokens)、[导入 API](https://api.labelstud.io/api-reference/api-reference/projects/import-tasks)和 [1.23.0 源码](https://github.com/HumanSignal/label-studio/blob/1.23.0/label_studio/data_import/api.py)共同支持：不能从 legacy token 被禁推导出“1.23 没有公开 API”；应区分 PAT refresh、Bearer 与 legacy Token 认证。
- [版本对比](https://labelstud.io/guide/label_studio_compare)和[用户文档](https://labelstud.io/guide/signup)明确社区版权限与审核工作流边界；社区版用户可见全部项目，外部复核清单不是内置 RBAC 审核系统。
- [导出文档](https://labelstud.io/guide/export)说明普通社区版 UI 导出不受页签筛选限制，且可包含取消的标注。训练前需依据批准清单选择最终 annotation。
- [7月工作](../../牛只数据集/7月工作.md)§2.3、§9.1 要求预测与人工标签分离，并记录了 CVBD-5 在暗光、遮挡场景下修正负担较高的历史情况；这不支持普遍的预标注效率提升结论。

## 冲突与限制

| 来源表述 | 核查后的适用范围 |
|---|---|
| 本地“Sync 会造坏任务” | 保留为特定实例经验；官方支持存储同步，手动 JSON 路线应避免重复建任务 |
| 本地“API 走不通” | 仅证明当时认证尝试受阻，不说明 API 缺失 |
| 旧笔记相对 Storage Path | 当前官方界面文档写 Absolute local path；任务 URL 的 `d` 参数仍是相对路径 |
| 通用安装页写较低 Python 版本 | 固定版本 1.23.0 应以 [PyPI 元数据](https://pypi.org/project/label-studio/1.23.0/)的 Python ≥3.10、<4 为准 |
| “导出后可直接训练” | 还缺最终结果选择、负样本确认、配对和坐标等数据验收 |

## 综合判断与待核实项

**综合判断：** Label Studio 在功能层面可支撑牛只水平框标注与预标注修正，适合先开展代表性试标。建议以离线预测导入起步，保留纯人工对照，并将提交、复核、发布分为不同状态。

**待核实：** 当前实例状态、图片实际访问、真实导入导出行为、人工总耗时、困难场景质量和并发体验。本次仅完成文档核查与示例检查，未操作远程实例或真实数据。

原始资料未修改；研究记录中的抽检比例、试标数量和复核表字段是方案建议。生成图仅作示意，不是实验结果。
