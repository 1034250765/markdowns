## 优先配置node.js



### CC SWITCH

可以把自己的模型接入到claude code





### 安装claude

```cmd
npm install -g @anthropic-ai/claude-code
```

输入以下命令查看是否安装成功

```cmd
claude -version
```

输入命令启动

```cmd
claude
```

对话框中输入/model 可以查看使用的模型



### 常用命令

| 命令        | 用途                                         |
| :---------- | :------------------------------------------- |
| `/login`    | 登录或注册账号                               |
| `/recharge` | 给账号余额充值                               |
| `/billing`  | 查看使用情况、余额和消耗概览                 |
| `/invoice`  | 查看账单、充值与消费记录                     |
| `/goal`     | 管理当前会话或阶段性目标，帮助长任务保持方向 |
| `/model`    | 查看并配置可用模型                           |

### 权限

Claude Code 内置了6种权限模式，每种模式的自主操作权限、适用场景都不一样，大家可以按需选择，不用盲目全开最高权限。

权限模式	核心能力（无需手动询问）	适用场景
default（默认模式）	仅支持读取文件、查看代码，所有编辑、命令操作都需手动批准	初次上手、陌生代码库、生产环境敏感操作，安全性最高
plan（规划模式）	仅读取、分析代码，只会输出优化/开发方案，不会改动任何代码	需求梳理、代码重构规划、方案评估，只看结果不改动项目
acceptEdits（编辑自动批准）	自动执行文件读取、代码编辑、基础文件操作（mkdir、touch、mv、cp等），Shell命令仍需确认	日常开发首选，信任AI代码编辑能力，同时规避高危命令风险
auto（智能自动模式）	支持全部操作，自带后台安全校验机制，自动拦截高危违规操作	长时间迭代开发、批量重构，大幅减少弹窗，兼顾效率与安全
dontAsk（严格受限模式）	仅允许提前手动配置、预先批准的工具操作，其余全部拦截	CI自动化流程、受限开发环境，极致安全管控
bypassPermissions（全权放行模式）	跳过所有权限校验和安全检查，几乎所有操作自动执行	仅适合隔离沙箱、本地测试环境，生产环境严禁使用
**shift+tab进行切换**

**可以在settings.json中配置allow和deny规则**

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(npm run lint:*)",
      "Bash(git diff:*)",
      "Bash(git status:*)",
      "Edit",
      "Read"
    ],
    "deny": [
      "Bash(git push --force:*)",
      "Bash(rm -rf:*)",
      "Bash(sudo:*)",
      "Bash(chmod:*)"
    ]
  }
}

```

**规则优先级**：项目本地配置（`.claude/settings.local.json`）> 项目配置（`.claude/settings.json`）> 全局配置（`~/.claude/settings.json`）。



你可以这样跟它说：“请在当前项目根目录下创建 .claude/settings.json 配置文件，采用 allow/ask/deny 的权限配置模式，先扫描分析项目的技术栈，然后自动允许安全的常用命令。

```cmd
# 查看当前 Claude Code 版本
claude --version

# 查看帮助
claude --help

# 配置权限（在会话中使用）
/permissions

# 启用 Auto Mode（需 Team 计划）
claude --enable-auto-mode

# 查看 Auto Mode 默认规则
claude auto-mode defaults

# 非交互模式一次性执行任务
claude -p "你的任务描述"

# 恢复之前的会话
claude --resume
```



### claude.md

想高效使用 Claude Code，仓库根目录的 CLAUDE.md 是最重要的文件。它是代理的“宪法”，也是理解仓库运作方式的首要依据。

如何维护这个文件要看场景。对个人项目，我基本放任 Claude 写入它认为必要的内容。

在工作中，我们在单仓库中严格维护 CLAUDE.md，目前约 13KB（很可能增长到 25KB）。



**建议在编码过程中至少运行一次 /context**，观察你的 20 万 Token 上下文窗口是如何被使用的（即使是 Sonnet‑1M，我也不太相信它能持续高效利用完整上下文）。在我们的单仓库中，新会话的基础开销约 2 万 Token（约 10%），剩余约 18 万用于具体改动——很快就会被占满。
**钩子（Hook）**
钩子非常重要。个人项目我用得不多，但在复杂的企业仓库中，它们对引导 Claude 至关重要。钩子与 CLAUDE.md 的“建议”互补，是“必须执行”的确定性规则。

我们使用两类钩子：

提交阶段阻断钩子：这是我们的主策略。一个包裹 Bash（git commit） 的 PreToolUse 钩子会检查 /tmp/agent-pre-commit-pass 文件——该文件只有在所有测试通过时由测试脚本创建。若文件缺失，钩子就阻断提交，迫使 Claude 进入“测试‑修复”循环，直到构建变绿。
提示钩子：这类钩子不阻断，仅提供“发射后不管”的轻量反馈；即便代理行为不尽如人意也不会强制阻止。






### 保留会话-保留对话

  ┌────────────┬─────────────────────────────────────────────────┐
   │    方式    │                      操作                       │
  ├────────────┼─────────────────────────────────────────────────┤
  │ --resume   │ 下次启动时加 --resume，会恢复上次的会话继续对话 │
  ├────────────┼─────────────────────────────────────────────────┤
  │ --continue │ 类似 resume，加载最近一次会话                   │
  └────────────┴─────────────────────────────────────────────────┘



### 安装skills

您可以通过在 Claude Code 中执行以下命令，将本仓库注册为 Claude Code 插件市场：

```python
/plugin marketplace add anthropics/skills
```

然后，安装一套特定的技能：

或者，可以通过以下方式直接安装任意一个插件：

```cmd
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

安装插件后，你只需提及这个技能即可使用。