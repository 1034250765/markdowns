# Claude操作指南 — 会话整理

> 会话时间：2026-06-08  
> 模型：deepseek-v4-pro[1m]

---

## 一、内置工具概览

Claude Code 的内置工具按类型分为：

| 类别 | 工具 | 功能 |
|------|------|------|
| 文件 | Read / Write / Edit / Glob / Grep / NotebookEdit | 读写、搜索、编辑文件 |
| 命令 | Bash | 执行 Shell 命令 |
| Web | WebSearch / WebFetch | 搜索网页、抓取 URL 内容 |
| 任务 | TaskCreate~List | 结构化任务管理 |
| 用户 | AskUserQuestion | 向用户发起选择题 |
| 定时 | CronCreate~List / ScheduleWakeup | 定时任务和唤醒 |
| 协作 | Agent / Workflow | 子代理和多代理编排 |
| Git | EnterWorktree / ExitWorktree | 隔离工作树 |

---

## 二、子代理（Agent）

### 核心概念
- 独立 AI 会话，并行执行，互不阻塞
- 每个 agent 有独立上下文窗口
- 结果返回给主会话，不会直接显示给用户

### 类型
| 类型 | 工具集 | 适用 |
|------|--------|------|
| general-purpose（默认） | 全部 | 通用任务 |
| Explore | 只读搜索 | 扫代码、找文件 |
| Plan | 只读（无编辑） | 设计实现方案 |
| claude | 全部 | 兜底通用 |

### 关键参数
- `run_in_background: true` — 后台异步执行
- `isolation: "worktree"` — 独立 git worktree（并行修改代码）
- `model` — 指定模型

### 管理命令
- `/agents` — 子代理仪表盘，查看进度/取消/看结果
- `/tasks` — 后台 Shell 任务管理

---

## 三、MCP（Model Context Protocol）

### MCP vs Bash 对比

| | Bash | MCP |
|------|------|------|
| 输入 | 命令字符串，易出错 | 强类型参数，自动校验 |
| 返回 | 原始文本流，需手动解析 | 结构化对象，直接用 |
| 依赖 | 需本地安装 CLI 工具 | 配好 MCP server 即可 |
| Context | 定义轻量，调用解析贵 | 定义重（一次性），调用省 |
| 适用 | 简单查询、一次性脚本 | 频繁操作、复杂参数 |

### MCP vs CLI（概念层面）
- MCP 是**协议标准**（类似 HTTP），CLI 是**软件产品**（类似浏览器）
- CLI 使用 MCP 来扩展能力

### MCP 与 GUI 应用

**核心结论**：不需要目标 GUI 提供 SDK，只需找到**某种程序化操控方式**。

五种操控手段：
| 方式 | 技术栈 |
|------|--------|
| OS 辅助功能 API | Windows UIA、macOS NSAccessibility、Linux AT-SPI |
| 窗口消息 | Win32 SendMessage |
| 键鼠模拟 | PyAutoGUI、xdotool、AppleScript |
| 图像识别 | OpenCV + Tesseract |
| 应用自带内部接口 | CDP(:9222)、VS Code API(:52340) |

Chrome DevTools MCP 真实案例：
- 截图 = 给 AI "视觉"
- CDP 协议 = 实际操作 DOM（点击/填表/读数据）
- Edge 同理，改成 `msedge.exe --remote-debugging-port=9222` 即可

---

## 四、Memory 记忆系统

### CLAUDE.md（指令记忆）
| 位置 | 范围 | 内容 |
|------|------|------|
| `~/.claude/CLAUDE.md` | 全局 | 个人偏好、语言习惯 |
| `./CLAUDE.md` | 项目 | 架构、技术栈、命令 |

- 优先级：项目覆盖全局
- 跨会话生效（磁盘文件，每次启动重读）

### Memory 文件（事实记忆）
- 位置：`~/.claude/projects/<项目路径>/memory/`
- 按工作目录隔离，同目录所有会话共享
- 四种类型：`user` / `feedback` / `project` / `reference`
- 通过 `MEMORY.md` 索引管理，`[[wikilink]]` 互相引用

### 全局记忆
- 位置：`~/.claude/memory/`
- 不绑定项目，任何工作目录都能加载

### CLAUDE.md vs Memory
- CLAUDE.md = 指令（怎么做），Memory = 事实（发生过什么）
- 前者稳定，后者持续增长

### 快捷命令
- `# 内容` — 等价 `/memory 内容`，快速记录
- `! 命令` — 在当前会话执行 shell 命令

---

## 五、Context 和 Compact

### /context 命令
查看当前会话 token 消耗分布（System prompt、Tools、MCP、Memory、Messages）

### Compact（压缩）
- **自动触发**，不由 AI 控制
- 流程：检测超标 → 提取最早对话 → 小模型生成摘要 → 替换旧对话
- 结果：早期细节丢失，核心保留，**不可撤销**
- AI 无法干预选择哪些内容被保留

### 用户对策
- 及时 `/context` 关注水位
- 长任务中途主动总结关键进展
- 重要信息写入 CLAUDE.md 或 Memory（持久化到磁盘）

---

## 六、Playwright MCP

### 安装
```bash
npm install -g @playwright/mcp
npx playwright install chromium
claude mcp add playwright -- npx @playwright/mcp
```

### Playwright vs WebSearch
| | WebSearch | Playwright |
|------|-----------|------------|
| 后端 | 搜索引擎 API | 真实 Chromium 浏览器 |
| 能力 | 搜索→标题+链接 | 搜索+点击+填表+截屏+读 DOM |
| 适合 | "搜一下 xxx" | "打开京东加购物车" |

### DeepSeek 无多模态下如何操作网页
DeepSeek 不能"看"图片，但 Playwright 通过三种方式绕过：
1. **Accessibility Snapshot** — 页面转结构化文本树（主力）
2. **JS 读 DOM** — 直接提取数据
3. **网络拦截** — 抓 API 返回的 JSON

### 重要限制
MCP 工具在**会话启动时一次性加载**，中途安装的不会热加载。必须重启 Claude Code 才能使用新工具。
`/clear` 只清对话历史，不会重载工具。

---

## 七、其他话题

- Edge 浏览器也支持 CDP：`msedge.exe --remote-debugging-port=9222`
- `/init` — 为项目初始化 CLAUDE.md
- `/ide` — 连接 IDE（如 VS Code）
- `/plugin marketplace add anthropics/skills` — 添加技能市场
- 权限模式 6 种：default / plan / acceptEdits / auto / dontAsk / bypassPermissions
