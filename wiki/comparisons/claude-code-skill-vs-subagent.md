---
id: claude-code-skill-vs-subagent
type: comparison
status: draft
created: 2026-09-18
updated: 2026-09-18
sources:
  - Clippings/黑马Vibe Coding零基础入门，vibecoding项目，涵盖Claude Code、Cursor、Codex、SDD、LangChain、Agent开发.md
  - python/claude.md
---

# Claude Code 中 Skill 与 Subagent 的区别

## 参与来源

- [黑马Vibe Coding 第19集：Claude Code 子代理（Subagent）开发实战](../sources/heima-vibe-coding-p19-subagent.md) — 黑马程序员视频课程转写，本页四个对比维度的主要出处。
- `python/claude.md`（第六节"子代理与工作流"）— 用户自写笔记，关于自定义 agent 创建方式、独立上下文与并行执行的记录，作为交叉印证（用户记录/二手整理）。

## 对比表

| 维度 | Skill（技能） | Subagent（子代理） |
|------|---------------|---------------------|
| 调用方式 | 手动：通过斜杠命令调用 | 主代理自动判断并调用（也可手动指定，具体命令待核实） |
| 运行上下文 | 在当前对话中执行 | 独立运行、有独立上下文；主会话聊天记录不传入，避免 agent 间记忆串扰 |
| 定位/用途 | 知识、快捷指令模板 | 专家角色（"数字员工"），可多个并行运行 |
| 存放位置 | `.claude` 下的 skills 文件夹 | `.claude` 下的 agents 文件夹 |

## 协作关系（综合）

- **先技能，后代理**：先开发技能，再开发 agent；agent 的 MD 中声明可使用的技能。技能是共享资源，subagent 不独享技能，只声明"我有哪些技能可用"。
- **触发链**：用户提出需求 → 主代理（Claude Code）判断由哪个 subagent 干活 → 委派并等待 → subagent 调用所需技能完成任务 → 结果返回主代理。
- **并行**：主代理可同时派多个 subagent 工作，是配置 subagent 的主要收益之一。
- **隔离收益**：subagent 的独立上下文意味着它只收到任务指令本身，不带主会话历史，避免记忆混乱。
- 用户笔记印证（`python/claude.md`）：自定义 agent 可通过 `/agents` 面板创建，本质是"描述什么时候用它、它擅长什么"；subagent 独立上下文窗口、可并行执行、最终文本作为结果返回主会话。

## 证据等级

- **事实**：对比表四个维度来自课程转写 [2:54]–[4:48]；其中"存放位置"与"手动指定调用"两处受转写噪音影响，细节需回看视频或查官方文档。
- **综合**：触发链与并行/隔离收益由本集演示过程归纳。
- **待核实**：手动调用 subagent 的具体命令形式；agents MD 的官方字段规范（课程演示中由 Claude 代写，未展示规范）。

## 关联

- 来源页：[黑马Vibe Coding 第19集](../sources/heima-vibe-coding-p19-subagent.md)
