## 智能代码补全：最常用的核心功能

Copilot 默认会根据代码上下文自动触发补全，操作快捷键是关键：

接受建议：按下Tab键，直接采纳当前灰色补全建议
切换下一个建议：Alt+)（Windows/Linux）/Option+)（Mac）
切换上一个建议：Alt+(（Windows/Linux）/Option+(（Mac）



## Copilot Chat 对话式开发

通过 Copilot Chat 实现自然语言与代码的交互，支持**问答、编辑、代理**三种模式，满足不同开发需求：

- 问答模式（Ask）：用于代码解释、问题排查、技术咨询，不修改代码，例：解释这段Python代码的逻辑
- 编辑模式（Edit）：针对当前文件进行修改，会生成代码比对，可选择是否接受，例：给这个函数添加参数校验
- 代理模式（Agent）：最强模式，可跨文件操作、执行终端命令、创建 / 修改文件，例：创建一个响应式的任务管理器网页，分离HTML/CSS/JS

**快捷指令**：Chat 窗口中可使用快捷符号快速引入上下文，提升回答精准度：

- `#`：引入代码块 / 文件 / 项目，如`#file`（当前文件）、`#function`（当前函数）、`#project`（整个项目）
- `@`：引入专属 AI 助手，如`@terminal`（终端相关）、`@github`（GitHub 相关）、`@vscode`（VS Code 相关）

在项目根目录创建`.github`文件夹，新建`copilot-instructions.md`文件，添加项目的编码规范、命名规则、技术栈要求等，Copilot 会根据该文件的内容生成符合项目规范的代码，示例：

```js
# 项目通用编码指南
## 代码风格
- 使用ES6+语法开发JavaScript/TypeScript代码
- 前端使用语义化HTML5标签，CSS采用Flex/Grid布局
## 命名规范
- 变量、函数使用camelCase命名
- 类、组件使用PascalCase命名
- 常量使用UPPER_CASE命名
## 其他要求
- 所有函数必须添加注释说明功能、参数、返回值
- 避免使用已废弃的API
```

