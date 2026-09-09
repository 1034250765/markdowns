# REST 与 RESTful

> 整理自 2026-09-09 与小0的对话。一句话版本：**REST 是一种 Web 架构风格（名词），RESTful 是个形容词，意思是"符合 REST 风格的"**。它俩不是两个竞争的技术，一个是理念，一个是对理念的践行。

## 一、REST 是什么

**REST（Representational State Transfer，表述性状态转移）**，由 Roy Fielding（HTTP 协议的主要作者之一）在 2000 年博士论文中提出。

注意三点：**不是协议、不是框架、不是工具**，它是一种「架构风格」（architectural style）——本质是一组设计约束，按这套约束设计出来的系统，就是 REST 风格的。

### 六大约束（严格来说全满足才算 REST）

| 约束 | 含义 |
|---|---|
| 客户端-服务器 | 职责分离，各自独立演进 |
| 无状态 Stateless | 请求自包含，服务端不记会话 |
| 可缓存 Cacheable | 响应可自带缓存策略 |
| 统一接口 Uniform Interface | URI 定位资源 + 标准动词 |
| 分层系统 Layered System | 可插入代理、网关、负载均衡 |
| 按需代码 Code-on-Demand | 服务端可下发脚本给客户端（可选） |

### 核心思想：一切皆「资源」

后端的一切数据都抽象成「资源」——牛只数据集、每张红外图片、每个标注框，都是资源。运转方式：

**一切皆资源 → URI 定位 → HTTP 动词操作**

名字里的 "Representational" 指：网上传输的是资源的**表述**（如 JSON 格式的牛只数据），而不是直接碰数据库。

示例（牛只检测后端 API）：

| 动词 | URI | 语义 |
|---|---|---|
| GET | `/cattle` | 查询牛只列表 |
| GET | `/cattle/42` | 查询 42 号牛 |
| POST | `/cattle` | 新增一头牛 |
| PUT | `/cattle/42` | 更新 42 号牛 |
| DELETE | `/cattle/42` | 删除 42 号牛 |

（cattle 单复数同形，天生适合当资源名）

### 无状态的理解

每个请求自带全部信息，服务器不保存「会话记忆」。

类比：像**自动售货机**——投币、出货、两清，机器不记得上一个顾客；而不是学校门口早餐摊老板记得你「老规矩不加香菜」。

实际工作中的例子：Label Studio 的 API 就是 RESTful 的——`GET /api/tasks` 拉标注任务、`POST /api/datasets` 建数据集，就是「资源 + 动词」的套路。

## 二、REST vs RESTful

| 维度 | REST | RESTful |
|---|---|---|
| 词性 | 名词 | 形容词 |
| 是什么 | 架构风格（一组设计约束） | "符合 REST 风格的" |
| 层面 | 理论 / 原则 | 实践 / 落地结果 |
| 典型说法 | "REST 要求无状态通信" | "这个 API 设计得很 RESTful" |

一组类比（风格 → 符合风格的成品）：

- 极简主义（设计风格）→ 极简风的装修
- 面向对象（编程范式）→ 面向对象的代码
- **REST（架构风格）→ RESTful API**

## 三、落到代码：RESTful vs 非 RESTful 设计

| 操作 | RESTful | 非 RESTful |
|---|---|---|
| 查列表 | `GET /cattle` | `GET /getCattleList` |
| 查单个 | `GET /cattle/42` | `GET /getCattleById?id=42` |
| 更新 | `PUT /cattle/42` | `POST /updateCattle` |
| 删除 | `DELETE /cattle/42` | `GET /deleteCattle?id=42` |

区别一眼可见：

- RESTful 的 URL 里只有**名词**（资源），动作全交给 HTTP 动词
- 非 RESTful 把动词塞进 URL，还滥用 GET 干写操作（GET 在语义上应该是安全、幂等的）

## 四、较真环节（智识诚实）

工程口语里的 "RESTful API" 大多只做到了「HTTP + JSON + 语义化 URL + 标准动词」，离 Fielding 论文里六大约束的严格定义有距离——比如统一接口里还要求**超媒体（HATEOAS）**，业界几乎没人真做，Fielding 本人都公开吐槽过很多所谓 RESTful API 根本不算 REST。

所以平时听到 "RESTful API"，理解成「REST 风格的 Web API」就行，别抠字眼。

## 一句话带走

**REST 是菜谱，RESTful 是照着菜谱做出来的菜。**
