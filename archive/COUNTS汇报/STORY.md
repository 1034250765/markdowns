# COUNTS 论文汇报 · 叙事逻辑

## ① 用户意图对齐

- **目标受众**：实验室组会 / 论文 reading 小组 / 科研汇报场合的研究生、导师、研究员；属于学术圈同行交流，非营销对外场合。
- **核心目标**：讲完后希望观众相信 COUNTS 数据集在「目标检测与多模态 grounding」两个被忽视的任务上提供了细粒度 OOD 评测价值；记住一个核心对比（IID 强 ≠ OOD 强）和一个反直觉现象（Gemini 利用 ICE 反而被偏置示例带偏）。
- **PPT 长度**：共 18 页（含封面 + 目录 + 结束页）。10-20 页预算中段偏上。
- **视觉调性**：学术可信 + 明亮活泼微调（清亮蓝紫渐变主色、宝蓝主导、点缀明黄/蜜橙，弱化标准学术风的严肃灰度，但保留证据驱动、文字优先）。
- **内容边界**：
  - **必讲**：COUNTS 三档核心数字、O(OD)² 关键结果、DINO/DINOv2 是表现最佳检测器、Gemini 在协变量偏移下从 57.0% 掉到 28.0%、ICE 是双刃剑。
  - **不讲**：附录的逐模型训练细节、术语对照全部表（仅挑核心几个放正文即可）、附录 D 局限性和 E 更广泛影响（合并成 1 句结论）。
  - **禁碰**：伪造实验数字、伪造论文作者、伪造日期；论文外的事实一概不引入。

## ② 页面布局骨架

- **总页数与分章**：18 页，分 5 章节
  - 第 1 章 · 引子（页 1-3）：封面、目录、章节扉页"研究动机"
  - 第 2 章 · 现有研究的不足（页 4-5）：研究问题 + 现有基准缺口
  - 第 3 章 · COUNTS 数据集（页 6-9）：章节扉页、三档数字、14 域示例、数据收集流程
  - 第 4 章 · 基准与实验（页 10-15）：章节扉页、O(OD)² 框架、OODG 框架、检测器对比、影响 OOD 因素、OODG 结果
  - 第 5 章 · 讨论与结论（页 16-18）：ICL 双刃剑、章节扉页、研究价值、致谢 Q&A
- **Hero 页定位**：1、3、6、10、16、18 = Hero 页（共 6 页，比例 33%——略偏上限，可以接受）；间隔均 ≥ 1 个 Supporting 页。
- **rhythm 曲线**：peak=1,3,6,10,16,18（扉页/Hero）；transition=2,5,9,13；valley=其余。
- **非对称版式预算**：18 页中至少 8 页用非对称（≥ 44%）。
  - 用非对称：3,4,6,7,8,10,11,14,16 = 9 页 = 50% ✅
  - 用对称：1,2,5,9,12,13,15,17,18 = 9 页（含对齐术语条目页 5）
- **对称版式预算**：N 卡片横排只用 1 次（第 9 页数据收集流程用四胶囊横排）。

## ③ 页面大纲

### 1. 封面（cover）
- **type**：cover
- **role**：hero
- **rhythm**：peak
- **layout**：全屏视觉 + 大标题
- **visual**：左侧学术风 LOGO 区 + 右侧大幅主标区，浅蓝渐变底
- **visual_role**：anchor
- **density**：字数约 60 / 图 0 / 留白约 35%
- **anti_pattern**：禁止印章 / 金色 / 烟花 / 党建红；禁止党政红金政务风
- **description**：报告 COUNTS：分布偏移下面向目标检测与 MLLM grounding 的大规模基准；副标题标注论文标题、来源、汇报日期。

### 2. 目录（catalog）
- **type**：catalog
- **role**：supporting
- **rhythm**：valley
- **layout**：左标题 + 右内容（编号条目列表）
- **visual**：L3 章节编号方块（仅作 L3 角标，无大图）
- **visual_role**：atmosphere
- **density**：字数约 80 / 图 0 / 留白约 30%
- **anti_pattern**：禁止使用圆球编号；禁止英文条目比中文更抢眼；禁止满屏 5+ 条卡片横排
- **description**：列出 5 大章节：研究动机 → 现有不足 → COUNTS 数据集 → 基准与实验 → 讨论与结论。

### 3. 章节扉页 · 研究动机（section）
- **type**：section
- **role**：hero
- **rhythm**：transition
- **layout**：左标题 + 右内容（大数字 + 文字）
- **visual**：L1 巨型数字"60%"+"70%"+窄描述区，体现 IID 与 OOD 性能差距
- **visual_role**：anchor
- **density**：字数约 120 / 图 1（数据卡）/ 留白约 30%
- **anti_pattern**：禁止四卡片预览；禁止与封面雷同的色块
- **description**：揭示核心矛盾——目标检测器与多模态大模型在 IID 场景下表现强劲，遭遇分布偏移却大幅下降；本汇报围绕这一矛盾展开。

### 4. 研究问题（content · 5b 三栏并列）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：非对称三栏（侧重"为何重要"）
- **visual**：L1 三张同款卡，每张一个关键词
- **visual_role**：evidence
- **density**：字数约 240 / 图 0 / 留白约 18%
- **anti_pattern**：禁止等宽四卡横排；禁止主色填充超过 1 张卡
- **description**：从三个角度说明 OOD 泛化的重要性：检测器在自动驾驶等真实场景降级明显；MLLM 受偏置示例带偏；grounding 是细粒度视觉理解关键但未被系统评测。

### 5. 现有基准缺口（content · 5h 关键词矩阵）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：上图标矩阵 + 下结论条
- **visual**：L1 2×3 矩阵（既有基准 vs 缺口）
- **visual_role**：evidence
- **density**：字数约 280 / 图 0 / 留白约 15%
- **anti_pattern**：禁止把矩阵塞进等宽卡片
- **description**：分两半：现有 OOD 基准多关注分类；目标级标注的细粒度基准仅有 COCO-C/COCO-O 等，规模小或合成扰动。填表式呈现缺口。

### 6. 章节扉页 · COUNTS 数据集（section · 数据 KPI）
- **type**：section
- **role**：hero
- **rhythm**：peak
- **layout**：居中金句/巨型数字（三联数）
- **visual**：L1 KPI 三联数：35 类 / 14 域 / 22.2 万张
- **visual_role**：anchor
- **density**：字数约 100 / 图 0 / 留白约 30%
- **anti_pattern**：禁止用小数字塞进柱状图角落；禁止把数字塞进 N 卡片横排
- **description**：核心一句话——COUNTS 是首个同时支持目标检测和 grounding 的真实世界 OOD 大规模细粒度标注数据集。

### 7. COUNTS 四个核心数字（content · 5e 数据强调）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：非对称双栏（左侧 4 个 KPI 占 55%，右侧洞察文字 35%）
- **visual**：L1 大数字
- **visual_role**：anchor
- **density**：字数约 220 / 图 0 / 留白约 18%
- **anti_pattern**：禁止把数字塞进图表卡；禁止等宽四卡片
- **description**：四个数字呈现 COUNTS 体量：222,234 张图像、1,196,114 个边界框、35 个类别、14 个自然分布域；强调每个域包含完整类别空间。

### 8. 14 个分布域分布（content · 大图配文）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：左大图 + 右侧文字
- **visual**：L1 SVG 标签云图（14 个域的标签分布）
- **visual_role**：anchor
- **density**：字数约 260 / 图 1 / 留白约 18%
- **anti_pattern**：禁止把全部域展开为表格；禁止等宽六卡横排
- **description**：按分布类型分组：环境类（snow/sand/grass/water/road/street/tree）、光照与遮挡（dim/occlusion）、风格化（painting/handmade）、特殊场景（indoor/mountain/sky），展示各域样本量分布。

### 9. 数据收集三阶段流程（content · 5c 流程时间轴）
- **type**：content
- **role**：supporting
- **rhythm**：transition
- **layout**：四胶囊横排 + 底部结论
- **visual**：L1 流程连接
- **visual_role**：evidence
- **density**：字数约 200 / 图 0 / 留白约 15%
- **anti_pattern**：禁止把每步展开为独立卡片
- **description**：候选筛选（500万+）→ 双人验证域标签 → 测试/验证集人工重新标注边界框（23,000 张）。强调"自然图像 + 人工标注"全流程。

### 10. 章节扉页 · 基准与实验（section）
- **type**：section
- **role**：hero
- **rhythm**：transition
- **layout**：全幅图 + 骑线文字（"两个基准"）
- **visual**：L1 双轨 SVG 示意（O(OD)² + OODG）
- **visual_role**：anchor
- **density**：字数约 110 / 图 1 / 留白约 30%
- **anti_pattern**：禁止密集文字；禁止重复第 3 页样貌
- **description**：本文提出两个基准——O(OD)² 评估目标检测器，OODG 评估多模态大模型 grounding 能力。

### 11. O(OD)² 基准设计（content · 关键词矩阵 2x2）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：左标题 + 右 2×2 矩阵
- **visual**：L1 SVG 矩阵（6 个目标域）
- **visual_role**：evidence
- **density**：字数约 240 / 图 1 / 留白约 18%
- **anti_pattern**：禁止等宽六卡横排
- **description**：选取 sky、occlusion、grass、water、dim、handmake 六个目标域，每个对应一类独特分布偏移：拍摄角度、遮挡、复杂背景、低光、艺术化物体。

### 12. OODG 基准设计（content · 5b 三栏并列+）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：非对称三栏（5 种评测设置）
- **visual**：L1 三栏同款卡（任务概览）
- **visual_role**：evidence
- **density**：字数约 280 / 图 0 / 留白约 18%
- **anti_pattern**：禁止等宽五卡横排
- **description**：三类任务 × 五种评测设置：Visual Grounding / Recognition and Localization / Visual and Semantic Mapping；Zero-shot / IID ICL / 协变量偏移 / 标签偏移 / 伪相关偏移。

### 13. O(OD)² 检测器结果（content · 表 2 + 洞察）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：图表 + 洞察
- **visual**：Chart(分组柱状图) + 表格
- **visual_role**：evidence
- **density**：字数约 220 / 图 1 / 留白约 12%
- **anti_pattern**：禁止把洞察塞进表格角落
- **description**：DINO/DINOv2 平均 OOD mAP 0.213，主表中最高；更强 neck/head 在跨域泛化中反而表现更弱；head 优化是 OOD 提升的关键路径。

### 14. OODG 结果总览（content · 非对称双栏）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：非对称双栏（左侧大表 + 右侧关键洞察文字）
- **visual**：Chart(双折线图，零样本 vs ICL 偏移) + 表格
- **visual_role**：evidence
- **density**：字数约 280 / 图 2 / 留白约 15%
- **anti_pattern**：禁止对称双栏等分；禁止仅看一张图就总结
- **description**：Visual Grounding 零样本：GPT-4o 0.659、Gemini 0.591、GLaMM 0.625；协变量偏移下 Gemini 从 57.0% 掉到 28.0%（50.88% 相对下降）；GPT-4o 下降较轻（最大 12.1%）。

### 15. 反直觉发现：ICL 双刃剑（content · 上下分栏）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：非对称双栏（两个模型对比 + 共同结论）
- **visual**：L1 对比卡
- **visual_role**：evidence
- **density**：字数约 280 / 图 0 / 留白约 18%
- **anti_pattern**：禁止 50:50 等分；禁止把观察笼统概括
- **description**：Gemini 善于利用 ICE，IID 下显著提升，但遇到分布偏移就被带偏，下降幅度远超 GPT-4o；GPT-4o 更稳健，ICE 利用率低。

### 16. 章节扉页 · 结论与价值（section · 居中金句）
- **type**：section
- **role**：hero
- **rhythm**：peak
- **layout**：居中金句/巨型数字
- **visual**：L1 居中金句（O(OD)² × OODG）
- **visual_role**：anchor
- **density**：字数约 80 / 图 0 / 留白约 40%
- **anti_pattern**：禁止满屏蓝红金；禁止重复前面 Hero 页结构
- **description**：以金句收束核心发现：IID 强不等于 OOD 强；ICE 是把双刃剑。

### 17. 研究价值 & 应用前景（content · 大图配文）
- **type**：content
- **role**：supporting
- **rhythm**：valley
- **layout**：上大图 + 下方三卡片
- **visual**：L1 应用场景图（自动驾驶/机器人/监控示意）
- **visual_role**：atmosphere
- **density**：字数约 240 / 图 1 / 留白约 18%
- **anti_pattern**：禁止堆满 4+ 同宽卡片
- **description**：自动驾驶、机器人、监控、内容审核等场景均需鲁棒的目标检测与 grounding；COUNTS 为这些场景提供评测基础设施。

### 18. 致谢 · Q&A（ending）
- **type**：ending
- **role**：hero
- **rhythm**：peak
- **layout**：全屏视觉 + 大标题
- **visual**：L1 中央居中标题（Q&A）
- **visual_role**：atmosphere
- **density**：字数约 60 / 图 0 / 留白约 50%
- **anti_pattern**：禁止金装饰 / 烟花 / 印章
- **description**：论文出处、代码与数据集链接、致谢作者与单位。

---

## 关键事实自检（讲稿层）

- 报告主题：COUNTS = Common Objects UNder disTribution Shifts
- 论文：arXiv:2504.10158（Jiansheng Li 等，清华）
- 三档核心数据：222,234 张图 / 1,196,114 框 / 35 类 / 14 域
- O(OD)² 最佳：DINO/DINOv2 平均 OOD mAP = 0.213
- OODG 关键反直觉发现：Gemini 在协变量偏移下从 57.0% 跌至 28.0%（相对 -50.88%）
- 代码：https://github.com/jiansheng-li/COUNTS_benchmark
- 数据：https://huggingface.co/datasets/jianshengli/COUNTS
- 汇报日期：2026 年 8 月
