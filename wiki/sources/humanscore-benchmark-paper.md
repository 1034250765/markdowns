---
id: humanscore-benchmark-paper
type: source
status: draft
created: 2026-09-18
updated: 2026-09-18
sources:
  - Clippings/HumanScore-Benchmarking-Human-Motions-in-Generated-Videos-arXiv-2604.20157.pdf
---

# HumanScore：生成视频人体运动质量基准（arXiv 2604.20157）

## 资料信息

- 类型：学术论文预印本（PDF 全文，正文约 14 页 + 附录，共 50 页）
- 标题：HumanScore: Benchmarking Human Motions in Generated Videos
- 作者：Y. Fang, T. Xiang 等（Stanford 团队；资助方含 NIH R01AG089169、P41EB027060、Panasonic、Stanford HAI、Stanford Wu Tsai Human Performance Alliance）
- 链接：<https://arxiv.org/abs/2604.20157>
- 提交日期：2026-04-22（arXiv）；导入日期：2026-09-18
- 本地路径：`Clippings/HumanScore-Benchmarking-Human-Motions-in-Generated-Videos-arXiv-2604.20157.pdf`

## 资料讲了什么

论文提出 **HumanScore**——首个系统性评测 AI 生成视频中**人体运动质量**的基准框架。核心论点：现有视频生成基准（VBench、T2V-CompBench 等）只衡量像素级真实感与语义对齐，而人体运动（解剖学、运动学、动力学合理性）仍是区分真假视频的关键信号。论文将生物力学三层体系转化为 6 个可量化指标，对 13 个 SOTA 视频生成模型打分，揭示"外观逼真"与"运动物理合理"之间的持续差距。

## 关键事实（带章节定位）

### 动机与技术时机（§1 Introduction）

- 生成模型在 VBench 等外观类基准上接近饱和，但观众仍能凭人体运动的不合理（解剖、运动学、动力学不可行/不一致）识别 AI 视频。
- 两个前置条件同时成熟：单目人体姿态/网格恢复在 3DPW 等基准上误差收敛饱和；生成模型在外观指标上饱和——使得从生成视频中可靠提取 3D 运动并做生物力学分析成为可能。

### 框架三组件（§3 HumanScore）

1. **动作集筛选**（§3.1）：以 Kinetics-700（700 类）为初始池，CLIP + SBERT 编码动作名、余弦相似度阈值 0.8 + 最远点采样（FPS）去重 → LLM 归类运动家族并验证覆盖类型（上肢/下肢主导、全身协调、翻转、自接触、物体交互）→ 实证可行性检查（剔除高失败率动作）。最终 **51 种动作 × 3 难度级（各 17 种）× 2 强度（gentle/intense）= 102 条 prompt**。
2. **Prompt 设计**（§3.2）：五要素标准化模板（场景 + 动作 + 强度 + 描述 + 相机），关键约束包括 "indoor studio with neutral background"、"full-body"、"Locked, static camera; the subject stays centered and unobstructed."、"A single person"；所有模型使用相同 prompt。
3. **指标设计**（§3.3）：生物力学三层六维，每层 2 个独立指标，归一化为 0–100 分：

| 层级 | 指标 | 衡量内容 | 实现方式 |
|------|------|----------|----------|
| 解剖正确性 | (I) 多余肢体 | 重复肢体、鬼影肢体 | HADM 异常肢体检测器 + 时序一致性检查 |
| 解剖正确性 | (II) 骨长一致性 | 刚体约束跨帧不变 | 2D→3D 关键点提升 → MeTRAbs 拟合 → OpenSim 表示；**故意解除模板骨长刚性约束**，计算相对中位长的 ℓ1 偏差 |
| 运动学正确性 | (III) 关节活动范围 | 关节角超出生理范围（超伸/屈曲） | OpenSim 骨架 + 生物力学标准限值 + 容差因子，统计越界幅度（均值与最大值） |
| 运动学正确性 | (IV) 自碰撞 | 肢体间不可能的互相穿透 | PromptHMR 生成 SMPL-X 网格，BVH 加速三角相交测试 + 非 local 过滤（区分轻度/重度碰撞加权求和） |
| 动力学正确性 | (V) 运动学极值 | 速度尖峰超过人类极限 | 中心差分求角速度 + 正向运动学求质心线速度，与每 DoF/每肢段限值对比 |
| 动力学正确性 | (VI) 运动平滑度 | 角加速度/jerk 异常（抖动、卡顿） | 基于 F=ma 将力约束转化为速度/加速度约束，对比每 DoF 限值 |

### 实验设计与主结果（§4–5）

- **被测模型 13 个**：开源 4 个（Wan 2.2、CogVideoX-5B、HunyuanVideo 1.5、Kandinsky 5.0 pro）+ 闭源 9 个（Sora-2、Veo 3.1 fast、KlingAI 2.5 Turbo Pro、Seedance 1.0 Pro fast、Hailuo 02、Pika v2.2、PixVerse 5.5、Ray 3.0、Wan 2.6）；另以真实视频（94.3 分）作为上界参照（Table 1）。
- **主排行榜**（Overall）：Seedance 1.0 Pro fast 与 HunyuanVideo 1.5 并列第一（91.1），KlingAI 2.5 Turbo Pro 次之（90.8）；CogVideoX-5B 垫底（74.8）。分维度：解剖最强为 HunyuanVideo 1.5（95.3）、Wan 2.2（94.0）、Seedance（93.9）；运动学最强为 KlingAI（86.4）；动力学最强为 KlingAI（95.1）、HunyuanVideo 1.5（94.9）、Seedance（94.3）。真实视频 94.3，与最强生成模型仍有明显差距。
- **与人类偏好对齐**（§4.2）：约 1200 份来自 AI 与生物力学社区的两两比较，HumanScore 与人工胜率的 Spearman 相关接近 1.0。
- **Real or AI 判别**（§4.3）：真实视频平均 94.3 分，高于所有生成模型，验证指标可区分真假；但真实视频也非满分（原因见"证据强度与限制"）。
- **与 VBench 的相关性**（§5.1，Table 2）：解剖/运动学维度与 VBench 外观轴 Spearman 相关 0.67–0.96，**动力学维度仅 0.19–0.35**——动力学真实性是现有外观类基准未覆盖的独立信息。
- **鲁棒性**（§5.2）：更换姿态估计器（时序优化 MeTRAbs / PromptHMR）后模型排名完全一致；容差扫描与聚合权重 (α,β,γ) 网格搜索下排名稳定。
- **主要发现**（§6.1）：视觉逼真 ≠ 运动真实；标准化 prompt 只能稳定评估条件、不能根治运动不合理的模型缺陷；各维度存在权衡（高动态模型牺牲解剖一致性，保守模型动作欠充分）。

## 证据强度与限制

- 论文为 arXiv 预印本，**尚未说明经同行评审**；排行榜数字随模型迭代会过时，引用时应注明评测时间点。
- 指标依赖外部模型（单目 3D 姿态/网格恢复 + 生物力学拟合），存在深度歧义、遮挡、运动模糊引入的估计噪声——**真实视频也拿不到满分（94.3 而非 100）**，论文在 §4.3 与 §6.2 中明确承认这一上限；部分极限柔术类动作会被保守的文献限值误伤。
- 动力学指标（V/VI）是间接代理：通过 F=ma 把力约束转化为速度/加速度约束，并非直接测量力学量。
- 动作集筛选中的实证可行性检查依赖特定生成器，动作池的选择标准部分来自作者主观与 LLM 判断。
- 本页数字均转录自论文 Table 1、Table 2 及正文，可回到 PDF 原文核对；论文图 7（人类偏好相关）的具体数值坐标未在文本中给出，仅报告"接近 1.0"，精确数值**待核实**。

## 关联

- 暂无其他 Wiki 页面链接到本页。候选关联方向（尚未建立，待后续资料导入时补充）：单目人体姿态/网格恢复（HMR）概念页；Kinetics-700 数据集实体页；视频生成评测基准（VBench）概念页。
- 用户自写资料 `牛只数据集/` 涉及动物（牛只）姿态估计与检测，与本文的"单目姿态估计误差收敛"前提属相邻技术领域，但无直接证据关联，不建立引用。
