---
id: heima-vibe-coding-p19-subagent
type: source
status: draft
created: 2026-09-18
updated: 2026-09-18
sources:
  - Clippings/黑马Vibe Coding零基础入门，vibecoding项目，涵盖Claude Code、Cursor、Codex、SDD、LangChain、Agent开发.md
---

# 黑马Vibe Coding 第19集：Claude Code 子代理（Subagent）开发实战

## 资料信息

- 类型：Bilibili 视频课程字幕转写（语音自动转写，噪音较多）
- 来源：黑马程序员《Vibe Coding 零基础入门》第 19 集（p=19）
- 链接：<https://www.bilibili.com/video/BV1RFTc62EaK?p=19>
- 发布日期：2026-07-01；剪藏日期：2026-09-18
- 本地路径：`Clippings/黑马Vibe Coding零基础入门，vibecoding项目，涵盖Claude Code、Cursor、Codex、SDD、LangChain、Agent开发.md`

## 资料讲了什么

本集演示在 Claude Code 中把上一节开发的单元测试技能（unit-test）分配给一个自定义子代理（subagent，课程称"数字员工/测试工程师"）的完整流程：先向 Claude 询问概念，再创建 agents 描述文件，重启生效后实测主代理自动委派。课程自述教学模式为 Vibecoding/SDD + 实战案例 + 动手开发（见剪藏开头简介段）。

## 关键事实（带视频定位）

- **架构比喻**：用户=项目经理，Claude Code 主代理=全栈工程师/老板，subagent=专家小组/虚拟数字员工；主代理可根据请求判断派哪个专家干活，也可同时派多个并行 —— [1:55]–[2:54]
- **调用方式差异**：技能（Skill）通过斜杠命令手动调用；subagent 由 Claude 自动判断并调用，也可以手动指定（转写含糊为"斜杠安静的命令"，具体命令形式待核实）—— [2:54]–[3:23]
- **上下文差异**：技能在当前对话中执行；subagent 独立运行、有独立上下文，主会话的聊天记录不传给干活的 subagent，以避免 agent 之间的记忆串扰 —— [3:23]–[4:20]、[9:36]–[10:32]
- **用途差异**：技能是"知识或快捷指令模板"；subagent 是"专家角色"，可并行运行多个以提升效率 —— [4:20]、[11:29]–[11:58]
- **存放位置**：技能存放在 skills 文件夹；agent 存放在 agents 文件夹（均在 `.claude` 目录下）—— [4:20]–[4:48]
- **创建方法**：在 `.claude` 文件夹内创建 `agents` 文件夹，每个 MD 文件描述一个专家；内容本质是自然语言，生成的示例结构包含：你是谁、能做什么、工作方式（调用哪个技能）、技术栈、重要规则、输出 —— [4:48]–[8:09]
- **技能共享**：subagent 不独享技能，技能是所有人共享的；只需在 subagent 的 MD 中声明它可以使用哪些技能（如 unit-test 单元测试技能）—— [5:17]
- **委派生成**：用户只需简单描述（名字 tester、用途为单元测试、可用技能 unit-test、触发时机为用户有单元测试需求时），Claude 会补全关键信息生成 MD；不满意可再让它修改 —— [5:46]–[7:40]
- **生效方式**：重启 VS Code（即重启 Claude Code）后重新读取设置，重新加载技能与 agent 列表 —— [8:38]
- **实测结果**：输入"帮我执行一下单元测试"后，主代理判断委派给 tester subagent 并等待其结果；主代理在等待期间不干活（"老板喝咖啡"）。因此前测试用例仍在代码中，subagent 无需重写代码、直接重跑即完成 —— [9:08]–[11:01]

## 证据强度与限制

- 本资料为视频语音自动转写，噪音大：多处术语误听——"sub edit / SAVAGINT / 沙包agent / SAYID"= subagent，"可乐code / 可乐 / CD / CLOOUD"= Claude Code，"SSCARE / SARE / square / scare"= Skill，"SABIG"= subagent。引用时应使用规范术语并回看视频核实。
- 转写未给出 agents MD 的具体字段名、frontmatter 格式与确切命令拼写，无法从本资料确认，属**待核实**；建议对照 Claude Code 官方文档或后续集数。
- **推断**：本集开头"上一小节完成了一个单元测试技能的开发"表明系列前一集（约 p=18）为 Skill 开发教程；该集尚未剪藏导入。
- 剪藏 frontmatter 中的简介还列出了同系列其他课程（AI 大模型开发、机器学习、深度学习等）的 BV 号，未在本集正文中展开。

## 关联

- 概念对比页：[Claude Code 中 Skill 与 Subagent 的区别](../comparisons/claude-code-skill-vs-subagent.md)
- 用户自写笔记 `python/claude.md` 第六节"子代理与工作流"记录了 `/agents` 面板创建自定义 agent 的方式，与本集"让 Claude 代写 MD"互为印证。
