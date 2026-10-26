---
id: playwriter-weiban-course-automation
type: concept
status: draft
created: 2026-10-26
updated: 2026-10-26
sources:
  - python/claude操作学习.md
  - python/Claude操作指南-会话整理.md
---

# 用 playwriter 驱动已登录 Chrome 完成麦课微课（weiban.mycourse.cn）

## 一句话结论

在 Chrome 守护进程运行、playwriter 扩展已连接的前提下，可以用「截图判断 + 元素坐标点击 + 直接触发播放器事件」的组合跑完安全教育微课的逐页交互。真正的难点不是"点哪里"，而是跨域 iframe 里的 CSS 缩放容器会让常规坐标 API 失真。

## 适用场景

- 网页课程平台：本例为安全教育类微课（外层 `weiban.mycourse.cn`，课程内容在 `mcwk.mycourse.cn` 的 iframe 里）
- 页面由图片热区 + jQuery 事件驱动，DOM 里没有语义化的按钮名，无法用常规选择器定位
- 需要沿用用户已登录的 Chrome 会话（而不新开浏览器或无登录态实例）

## 环境与连接

- 本机 npx 中已有 playwriter（本例 0.9.0），但命令不在 PATH，需用 `npx playwriter@latest ...`
- Chrome 必须已在运行；`session new --tab-group <名字>` 输出 `Extension connected` 表示扩展已连上
- 复用用户已打开的标签页（`context.pages().findLast(p => p.url().includes(...))`），不要另开浏览器
- 命令与规则以平台 skill 文档（`playwriter skill`，需完整阅读）为准

## 关键技术点

### 1. iframe 内坐标必须用元素自身的 getBoundingClientRect()

- **现象**：课程 iframe 的外层容器带 `transform: scale(0.7977)`（750×1206 设计稿缩放到 598×962）。此时 Playwright 的 `locator.boundingBox()` 返回失真坐标——翻页图片报 `y=-802`、页脚按钮报 `y=1412`，而元素实际在屏幕 `y≈870` 附近。按失真坐标去点，等于点在屏幕外，表现为"点了没反应"。
- **做法**：在 frame 内 `el.getBoundingClientRect()` 取中心点，再 `page.mouse.click(cx, cy)`。当 iframe 铺满整个视口时，frame 内的 CSS 坐标约等于页面坐标（本例 iframe 位于 (0,0)，尺寸 2048×962）。
- **副产品**：截图是 2560×1203 像素（DPR 1.25），人眼从预览图估算坐标时要按 ×1.0917 换算到 CSS 像素。

### 2. 翻页优先派发原生 click，而不是按坐标点

播放器使用 jQuery 委托事件（`$(this).parents(".page-item").next().addClass("page-active").siblings().removeClass("page-active")`），因此对活动页里的元素调用 `el.click()` 就能触发，不受动画位移、坐标失真的影响：

| 元素 | 作用 |
|---|---|
| `section.page-active .btn-next` | 标准翻页 |
| `.btn-next-4`、`.btn-next-end` | 特殊跳转 / 尾页（触发课程完成） |
| `.btn-af` | 答错后的「返回重选」 |
| `.btn-aq` | 提交本题答案 |

注意：jQuery 场景下原生 click 有效，这与"React 需用 Playwright 的 click 才能更新状态"的结论不同，判断依据是事件绑定方式而不是框架名字。

### 3. 课程页常见交互类型（需逐类处理）

| 类型 | 识别特征 | 处理方式 |
|---|---|---|
| 普通内容页 | 活动页内有 `.btn-next` | 直接点 |
| 长文页 | 存在滚动容器（如 `.simplebar-content-wrapper`） | 滚动到底后再找按钮 |
| 视频页 | 活动页内有可见 `<video>` | 等播放结束（本例按 1x 正常速度，未用倍速） |
| 图片热区页 | 只有 `<img>`/`<div>`，没有按钮类名 | 按截图坐标点（如「点击链接」「看这个」） |
| 多图各点一次 | 源码里 `clickedStates` 记录点击，全部点过才显示 `btn-next` | 逐个点开并关闭浮层 |
| 标签切换页 | 多个分类标签 | 逐个点开 |
| 留言墙 | `textarea` + `.message-submit` | 必须先发布评论，成功后 `.page-17 .btn-next` 才 `display:block` |

### 4. 答题页

- 单选/多选：选项是 `.aq-item-label` 下的 `input`，点 input 后再点 `.btn-aq` 提交
- 答错不会直接卡死，而是进入 `afXX` 解析页，点 `.btn-af` 返回重选
- 题目文案本身是可读文本（不是图片），可直接从 `document.body.innerText` 提取，不必逐张截图

### 5. 考试页（同站 exam-page）

- 结构：35 道单选 + 15 道多选，共 50 题；答题卡按题型分别从 1 开始编号（单选 1–35、多选 1–15），对应全局题号需换算
- 直接点「下一题」会弹「请作答当前题目！」阻止跳过；改用「答题卡」点题号可以自由跳题，因此能在**不答题**的情况下遍历全部题目

## 风险与边界

- 平台随时可能改版：本页的类名与流程来自本轮实测和同站 `item.js` 源码，不具备长期稳定性
- 公开副作用：留言墙必须发评论才放行，评论会以匿名昵称对外可见
- 答题正确性取决于知识判断，不保证满分；本轮曾有 1 道多选被判错后重选
- 不代替用户执行「交卷」这类不可逆操作，选项勾选与提交仍由用户自己确认

## 证据等级

- **事实**：坐标失真现象与 `getBoundingClientRect` 修复、`.btn-next`/`.btn-af`/`.btn-aq`/`.message-submit` 的用途、以及"发布评论后才显示下一页"（`item.js` 中 `$(".page-17 .btn-next").css("display","block")`）均在本次实测或源码阅读中直接观察到。
- **综合**：各类页面处理清单由本轮 7 门课逐页处理后归纳。
- **推断/待核实**：其他同类 H5 微课平台是否同构未验证；`transform: scale()` 容器导致 Playwright bbox 失真的具体触发条件（何种嵌套层级）未完全定位。

## 关联

- 本页没有对应的 wiki 来源摘要页；原始记录为用户自写的 Playwright / playwriter 使用笔记：`python/claude操作学习.md`、`python/Claude操作指南-会话整理.md`。
- 同站一次完整实操结果（课程学习 24/31 → 31/31）属于本次会话事实，不另建实体页。
