## FastApi框架简介

**天生支持异步**

自动生成可交互文档

适用于API,微服务，AI推理

FastApi是一个基于python的高性能web框架，专门用于快速构建API接口服务。

![image-20260316155323274](images/image-20260316155323274.png)

![image-20260316155425986](images/image-20260316155425986.png)





## 第一个FASTapi程序

```python
from fastapi import FastAPI



# 第一个实例
app = FastAPI()


@app.get("/")        #根目录
async def root():    # sync同步 async异步
    return {"message": "Hello World666"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
# 启动fastapi
uvicorn backend.app.main:app --reload --port 8000

```

```cmd
uvicorn main:app --reload --port 8000

#在url中输入http://127.0.0.1:8000/docs
可以打开可交互文档页面
```

## 路由--URL与处理结果之间的映射关系

可以帮助我们访问不同的地址，得到不同的结果

```python
@app.get("/")        #根目录 app实例 get方法
async def root():    # sync同步 async异步
    return {"message": "Hello World666"}
```

## URL传参--路径参数

![image-20260316192632542](images/image-20260316192632542.png)

```python
#路径参数
@app.get("/hello/{name}")
async def say_hello(name: str):       #添加一个同名的形参
    return {"message": f"Hello {name}"}

#带类型的路径参数
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
#带Path限制的路径参数
from fastapi import FastAPI, Path
@app.get("/word_hello/{name}/{age}")
async def say_word_hello(name: str, age: int = Path(..., ge=1, le=100,description="年龄",min_length=1,max_length=3)):
    return {"message": f"Hello {name}, your age is {age}"}  
```

![image-20260316202935632](images/image-20260316202935632.png)

## 查询参数

![image-20260316203439232](images/image-20260316203439232.png)

```python
@app.get("/word_hello_world/")
async def say_word_hello_world(name: str = Query(...,description="姓名",min_length=1,max_length=3) ):
    return {"message": "Hello World"}
#查询参数可设置默认值，把...换成需要的默认值就可以
```

## 请求体参数

![image-20260317151111348](images/image-20260317151111348.png)

```python
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel       #从pydantic import BaseModel 


from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(...,description="姓名",min_length=1,max_length=3)   
    pwd: str = Field(...,description="密码",min_length=1,max_length=3)
    
    
@app.post("/login")    #POST方式请求
async def login(user: User):
    return user
```

## 请求对象体系（参数家族总览）

前面讲的路径参数、查询参数、请求体参数，本质都汇入同一个体系：FastAPI 有一套统一的**参数来源推断规则**，把请求的所有入口（路径、查询串、请求头、Cookie、body）收敛到一张表里。理解这张表，比逐个背 API 有用得多。

**家族谱系**

| 入口 | 从哪读 | 典型用途 |
|---|---|---|
| `Path()` | 路径模板 `/items/{id}` | 资源 id + 范围校验 |
| `Query()` | URL `?key=value` | 分页、筛选、排序 |
| `Body()` | 请求体 JSON | 多模型、嵌套结构 |
| `Header()` | 请求头 | 自定义头、鉴权 token |
| `Cookie()` | Cookie | session、偏好设置 |
| `Form()` | 表单编码的 body | HTML 表单提交 |
| `File()` | `multipart/form-data` | 文件上传 |
| `Depends()` | 依赖函数的返回值 | 复用逻辑、鉴权、DB session |
| `Request` | 原始报文（不走推断） | 逃生舱 |

**核心机制：参数来源的自动推断规则**

FastAPI 拿到函数签名后，逐个形参判断它该从哪读——**大多数情况不需要你主动声明**：

| 形参长什么样 | 判定为 | 从哪读 |
|---|---|---|
| 名字出现在路径模板 `{...}` 里 | 路径参数 | URL 路径 |
| 类型是 Pydantic `BaseModel` | 请求体 | JSON body |
| 类型是标量（`str`/`int`/`float`/`bool`/`datetime`/`UUID`…） | 查询参数 | `?key=value` |
| 默认值写的是 `Depends(...)` | 依赖 | 依赖函数的返回值 |

```python
@app.get("/items/{item_id}")            # ← 路径里有 item_id
async def read_item(
    item_id: int,                       # ① 名字在路径里 → 路径参数
    q: str | None = None,               # ② 标量类型   → 查询参数
    user: User = None,                  # ③ BaseModel  → 请求体
    token: str = Depends(verify),       # ④ Depends    → 依赖
):
    ...
```

`Path()` / `Query()` / `Body()` 的作用是在推断结果之上**追加校验规则和文档描述**；而 `Header()` / `Cookie()` / `Form()` / `File()` 是**必须显式写的**——不写的话，一个 `str` 形参默认会被当成查询参数，去 URL 里找，而不是去请求头里找。

**推论**

1. **同一个形参名，加不加 `Header()` 决定它从哪来**。`token: str` 会去 URL 里找 `?token=...`；`token: str = Header()` 才会去请求头里找。
2. **`Request` 对象是唯一绕过整套推断的入口**，它不参与上面的判定，永远直接拿到原始报文。
3. **形参名必须和路径模板里的占位符完全一致**。`@app.get("/items/{item_id}")` 要配 `item_id: int`，写成 `id: int` 会报缺参数。

**逃到 Request 对象：体系之外的那扇门**

需要原始报文本身（而不是某个已被解析好的字段）时，在函数签名里写 `request: Request`，FastAPI 会自动注入（不用手动构造）。它把 HTTP 报文封装成一堆好用的 Python 属性：

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/cows/{cow_id}")
async def update_cow(cow_id: int, request: Request):
    request.method                 # "POST"
    request.url.path               # "/cows/42"
    request.path_params            # {"cow_id": "42"}   ← 注意是字符串
    request.query_params           # ?page=2 → {"page": "2"}
    request.headers["user-agent"]  # 大小写不敏感
    request.cookies                # {"session": "abc"}
    request.client.host            # "127.0.0.1"

    body = await request.json()    # 读请求体，必须 await
    return {"ok": True}
```

**属性 ↔ 报文的对应关系**

| 报文位置 | Request 属性 |
|---|---|
| 请求行 | `.method` / `.url` |
| 请求头 | `.headers` / `.cookies` |
| URL 查询串 `?page=2` | `.query_params` |
| 路径模板 `/cows/{id}` | `.path_params` |
| 请求体 | `await .json()` / `.form()` / `.body()` |
| 客户端信息 | `.client`（host + port） |
| 应用实例 | `.app`（就是那个 FastAPI 对象） |

**三个坑**

1. **读 body 是异步的**。`.json()` / `.body()` / `.form()` 都要 `await`。底层 ASGI 的消息流本身只能消费一次，但 **Starlette 的 `Request` 对象自带缓存**（`_body` / `_json` / `_form`），所以**在同一个 request 对象上**重复调这几个方法是安全的。真正会翻车的是这三种情况：① 用 `request.stream()` 直接迭代流——流不缓存，消费掉就没了；② 在中间件里消费了 receive 流，导致下游拿到空 body；③ 两个不同的 `Request` 对象之间缓存不共享（比如在中间件里手动 `Request(scope, receive)` 新建了一个）。
2. **`.path_params` 的值是字符串**。`{"cow_id": "42"}` 而不是 `42`。函数签名里那个 `cow_id: int` 是 FastAPI 另外帮你转的，两处拿到的不是同一个东西。
3. **`.query_params` 也全是字符串**。`?page=2` 拿到 `"2"`，参与计算前自己 `int()`。

**request.state —— 跨中间件传值**

中间件里往 `request.state` 塞东西，路由函数里取出来。这是传递上下文（trace id、当前用户、DB session）的标准做法：

```python
from uuid import uuid4

@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    request.state.trace_id = uuid4().hex       # 中间件里塞
    response = await call_next(request)
    response.headers["X-Trace-Id"] = request.state.trace_id
    return response

@app.get("/x")
async def x(request: Request):
    return {"trace": request.state.trace_id}   # 路由里取
```

**什么时候用它，什么时候用声明式参数**

| 场景 | 用什么 |
|---|---|
| 要某个字段，类型明确 | 声明式（形参 + 类型注解） |
| 要看原始 header / cookie 全貌 | `request.headers` / `request.cookies` |
| 要拿客户端 IP、原始 URL | `request.client` / `request.url` |
| 中间件里读写请求上下文 | `request.state` |
| 要读原始 body 自己解析 | `await request.body()` |

原则：**能用声明式就用声明式**（有校验、有自动文档），`Request` 留给框架没提供声明式入口的角落。

**表单与文件上传：Form() 与 File()**

这两种请求体上面没讲，因为它们**不是 JSON**，而且需要额外依赖（不装会直接报 `RuntimeError: Form data requires "python-multipart"`）：

```bash
pip install python-multipart
```

```python
from fastapi import FastAPI, Form, File, UploadFile

# 纯表单：Content-Type 为 application/x-www-form-urlencoded
@app.post("/login/form")
async def login_form(
    username: str = Form(...),
    password: str = Form(...),
):
    return {"username": username}

# 表单 + 文件：Content-Type 为 multipart/form-data
@app.post("/upload")
async def upload(
    cow_id: int = Form(...),
    image: UploadFile = File(...),
):
    return {"filename": image.filename}
```

**注意：`Form()` 和 `Body()` 不能混用**。一个请求的 body 只能有一种编码——要么是 JSON（配 `Body()` / Pydantic 模型），要么是表单（配 `Form()` / `File()`），混着写启动就会报错。

**UploadFile：不要用 bytes 接文件**

`File()` 也能配 `bytes` 用（`image: bytes = File()`），但**大文件别这么写**——`bytes` 会把整个文件读进内存。`UploadFile` 才是正解：

| 属性 / 方法 | 说明 |
|---|---|
| `.filename` | 客户端传来的原始文件名 |
| `.content_type` | 如 `image/jpeg` |
| `.size` | 字节数（较新版本才有） |
| `await .read(n)` | 读 n 字节，**异步** |
| `await .seek(0)` | 回到开头，可重复读 |
| `await .write(data)` | 写入 |
| `.file` | 底层的类文件对象 |

关键在底层：`UploadFile` 包的是一个 `SpooledTemporaryFile`——**数据先在内存里，超过阈值（默认 1MB）自动落盘**。所以：

- 传一个 2GB 的模型权重上来，服务不会 OOM
- 读取是异步的，不阻塞事件循环
- 要直接转交给第三方库（PIL、numpy）时，用 `image.file` 拿底层对象，省一次拷贝

```python
from PIL import Image

@app.post("/detect")
async def detect(image: UploadFile = File(...)):
    img = Image.open(image.file)     # 直接喂给 PIL，不用先读成 bytes
    await image.seek(0)              # 要重复读就先 seek 回开头
    return {"size": img.size}
```

**几个细节**

- **`Header()` 默认把形参名里的 `_` 转成 `-`**：`user_agent: str = Header()` 读的是 `User-Agent` 头。要禁用转换写 `Header(convert_underscores=False)`。
- **形参名和 Python 关键字冲突、或想换个名字，用 `alias`**：`Query(alias="class")`。
- **只有一个 Pydantic 模型参数时，它直接就是整个 body**；有**两个及以上**时，FastAPI 自动按参数名嵌一层：`{"item": {...}, "user": {...}}`。想强制单模型也嵌一层（避免和前端的约定打架），用 `Body(embed=True)`。
- **现代写法推荐 `Annotated`**，把校验规则和类型注解合并在一起，抽出去复用时更干净：

  ```python
  from typing import Annotated

  async def read_item(q: Annotated[str | None, Query(max_length=50)] = None):
      ...
  ```

- **请求体是 JSON 时 `Content-Type` 必须是 `application/json`**，否则 FastAPI 会当成空 body 处理，直接抛校验错误——调试前端回调时最容易忽略的一条。

## 原理：FastAPI 怎么读到你的声明

前面反复强调「标签必须写在签名里」「FastAPI 在启动时扫描」。这一节把底层的两样东西讲清楚：**`__annotations__` 和 `inspect.signature`**。理解之后，「写在函数体里没用」就不再是需要背的规则，而是自然结果。

**一、`__annotations__`：函数自带的一张类型标签纸**

Python 执行 `def` 语句时，会把参数的类型注解求值，存进函数对象的 `__annotations__` 字典：

```python
def f(a: int, b: str = 'x') -> bool: ...
f.__annotations__
# {'a': <class 'int'>, 'b': <class 'str'>, 'return': <class 'bool'>}
```

三个反直觉的点：

- **值是真正的类型对象**，不是字符串（除非开了 PEP 563，见第四节）
- **返回值注解也在里面**，键名是字符串 `'return'`
- **注解是表达式，会被求值**：`def g(x: 1 + 2): ...` → `{'x': 3}`（真的算了一遍）

三个作用域各有一份：模块级 `__annotations__`、类级 `C.__annotations__`、函数级 `f.__annotations__`。FastAPI 读的是函数级那份。

**二、`inspect.signature`：把名字、类型、默认值对齐**

光有 `__annotations__` 不够——它只有类型，不知道"哪个参数有什么默认值"。所以 FastAPI 用 `inspect.signature()` 把三样东西打包成一条条记录：

```python
import inspect

def route(fn):
    for name, p in inspect.signature(fn).parameters.items():
        print(name, p.annotation, p.default)

@route
def read_item(item_id: int, q: str = Query(None)):
    ...
```

输出（实测）：

```
item_id <class 'int'>  <class 'inspect._empty'>
q       <class 'str'>  <Query ...>
```

看到了吗——`p.default` 里躺着的就是那个 `FieldInfo`（`Query` 实例）。FastAPI 遍历这些记录，按下面的规则分派：

| 判断 | 结论 |
|---|---|
| `p.default` 是 `FieldInfo` 实例 | 读出它的 `in_`，确定数据来源 |
| `p.default is inspect._empty` | 参数**必填**（没写默认值） |
| 名字出现在路径模板 `{...}` 里 | 路径参数 |
| `p.annotation` 是 `BaseModel` | 请求体 |

注意 `Path(...)` 里那个 `...` 是 `Ellipsis`，FastAPI 把它和 `inspect._empty` 一样当"必填"处理。

**三、所以你能手写一个迷你 FastAPI**

```python
import inspect
from typing import get_type_hints

def route(fn):
    hints = get_type_hints(fn)
    for name, p in inspect.signature(fn).parameters.items():
        print(f'{fn.__name__}.{name} -> {hints.get(name)}')
    return fn

@route
def read_item(item_id: int, q: str = None):
    ...
```

十几行代码就是 FastAPI 参数系统的骨架，剩下的活只是把读出来的东西接到 ASGI 请求上。

**四、PEP 563 会让注解变成字符串**

```python
from __future__ import annotations      # 必须在文件第一行

def f(a: int) -> bool: ...
f.__annotations__     # {'a': 'int', 'return': 'bool'}   ← 字符串了
```

这时必须用 `typing.get_type_hints(f)` 才能还原成真类型。**FastAPI 内部就是这么做的**，所以两种情况都能处理；但自己写反射代码时忘了这一步，就会拿到字符串。

（Python 3.14 起注解改为惰性求值 PEP 649，实现方式变了，`__annotations__` 的对外行为保持一致。）

**五、对照 C++：为什么这套在 C++ 里不成立**

Python 的函数在运行时仍携带说明书（`__annotations__` + `__defaults__`），所以能事后翻阅。

C++ 编译后类型擦除，只剩机器码，运行时无元数据可读。它只能在**编译期**用宏抢先收集：

```cpp
CROW_ROUTE(app, "/items/<int>")      // 宏展开时就把路由登记好
([](int id) { return "hi"; });
```

| | FastAPI | Crow / Drogon |
|---|---|---|
| 信息收集时机 | **运行时**（导入模块时） | **编译期**（宏展开时） |
| 手段 | 反射：`__annotations__` / `inspect` | 宏：文本替换 |
| 出错时间 | 启动时报错 | 编译时报错 |

注：Java 虽然也是编译型，但注解和类型信息会写进 class 文件，运行时反射可读——所以 Spring 的 `@GetMapping` 和 FastAPI 是同一个思路。**分水岭不是"脚本语言 vs 编译语言"，而是类型信息有没有留到运行时。**

**六、一条实用推论**

因为整套机制发生在**导入模块时**，所以：

| 错误写在哪 | 什么时候炸 |
|---|---|
| 装饰器参数 / 类型注解 / 标签用法 | **导入时就报错**，服务起不来 |
| 函数体里的代码 | 服务正常启动，请求来了才 500 |

`Form()` 和 `Body()` 混用、路径模板里有 `{x}` 但签名里没 `x`，都属于第一类。所以「启动成功」不等于「接口能跑通」——写完路由先用 `/docs` 点一遍，比等前端反馈高效得多。

## JSON响应格式

![image-20260317153244230](images/image-20260317153244230.png)

**默认响应json格式。**

## HTML响应格式与文件响应格式

![image-20260317153625700](images/image-20260317153625700.png)

```python
# 装饰器指定响应类
from fastapi.responses import JSONResponse, HTMLResponse

@app.get("/html", response_class=HTMLResponse)
async def html():
    return """
    <html>
        <head>
            <title>Hello World</title>
        </head>
        <body>
            <h1>Hello World</h1>
        </body>
    </html>
    """


# 返回响应对象
@app.get("/file")
async def file():
    return FileResponse("PixPin_2026-03-15_23-11-46.png")




```

## response_model 约束响应结构

这一节用的是 `response_model` 参数：**不改变输出格式（最终还是 JSONResponse），只对返回的数据做质检**——校验字段类型、过滤多余字段（隐藏密码等敏感字段的标准手法）。

```python
#先定义需要的类型
class User1(BaseModel):
    id : int = Field(...,description="用户id",min_length=1,max_length=3)
    name: str = Field(...,description="姓名",min_length=1,max_length=3)   
    title: str = Field(...,description="职称",min_length=1,max_length=3)
    content: str = Field(...,description="内容",min_length=1,max_length=3)
    
    
#
@app.post("/user1", response_model=User1)
async def get_user1(user_id: int):
    if user_id == 1:
        raise HTTPException(status_code=404, detail="用户id不存在")
    return {"id": user_id, "name": "张三", "title": "工程师", "content": "这是一个测试数据"}

@app.post("/user1", response_model=User1)
async def get_user1(user_id: int):
    
    user_id = User1(id=user_id, name="张三", title="工程师", content="这是一个测试数据")

    return user_id
```





## 响应对象体系（Response家族总览）

前面的 JSON / HTML / 文件响应和 response_model 约束，本质都汇入同一个体系：全部继承自 **`Response` 基类**（来自 FastAPI 的底层框架 Starlette，`from fastapi.responses import Response`）。

**家族谱系**

| 类 | 干什么 | 典型场景 |
|---|---|---|
| `Response` | 基类：content + status_code + headers + media_type | 自定义子类的父类 |
| `JSONResponse` | dict → JSON 序列化 | **默认包装器**，`return dict` 走的就是它 |
| `HTMLResponse` | 字符串按 text/html 发 | 返回页面片段 |
| `PlainTextResponse` | 纯文本 | 健康检查、robots.txt |
| `RedirectResponse` | 302/307 + Location 头 | 登录跳转、接口迁移 |
| `StreamingResponse` | 生成器逐块发（chunked 编码） | SSE 日志流、大文件边读边发 |
| `FileResponse` | 不读进内存，服务器直接发文件句柄；自动带 Content-Length / ETag，支持 Range 断点续传 | 文件下载**优先用它** |

**核心机制：return 值的自动转换规则（只有两条）**

```python
@app.get("/a")
async def a():
    return {"x": 1}      # 规则1：普通值 → FastAPI 用默认包装器(JSONResponse)
                          # 序列化后发出

@app.get("/b")
async def b():
    return JSONResponse({"x": 1}, status_code=201)
                          # 规则2：Response 实例 → 原样发出，FastAPI 不做任何加工
```

推论：一旦手动 return Response 对象，`response_model` 的序列化和文档化就被绕过了——发什么客户端收什么。

**改状态码/响应头的推荐姿势：依赖注入临时 Response 对象**

```python
@app.get("/login")
async def login(response: Response):    # 注入的是 fastapi.Response 临时对象
    response.status_code = 201
    response.headers["X-Custom"] = "yes"
    response.set_cookie(key="session", value="abc", httponly=True)
    return {"ok": True}                 # return 的 dict 仍会被自动序列化，
                                         # 但对 response 的修改会合并进最终响应
```

这种方式比手动构造 JSONResponse 好：不破坏 response_model 的自动文档。

**三个高频翻车点**

1. **参数注入的 `response` 不要拿去 return**。签名里写了 `response: Response` 时，它只负责「加料」（header / cookie / status_code），body 仍然靠 return 的普通数据生成。写成 `return response` 会得到一个空 body——因为你返回了一个自己没往里写内容的 Response 对象。
2. **`JSONResponse` 手工序列化遇到特殊类型会炸**。它内部走 `json.dumps`，碰到 `datetime`、`UUID`、Pydantic 模型直接 `TypeError`。两种解法：用 `fastapi.encoders.jsonable_encoder()` 先包一层，或换成 `ORJSONResponse`。
3. **手动返回 Response 会连带 `response_model` 和 `/docs` 的响应 schema 一起失效**（前面推论里提过）。真要用就顺手补上 `responses={200: {...}}` 显式声明，别让文档留个洞。

**换默认包装器的两种方式**

```python
# 方式1：装饰器参数（对整个接口生效，文档自动更新）
@app.get("/page", response_class=HTMLResponse, status_code=201)

# 方式2：应用级全局默认
from fastapi.responses import ORJSONResponse   # 高性能JSON，需 pip install orjson
app = FastAPI(default_response_class=ORJSONResponse)
```

**自定义 Response 子类：覆写 render()**

```python
class XMLResponse(Response):
    media_type = "application/xml"
    def render(self, content) -> bytes:
        return xml_dumps(content).encode()

@app.get("/data", response_class=XMLResponse)
async def data():
    return {"x": 1}      # 自动走 XML 渲染
```

**StreamingResponse：边产生边发送**

接收一个异步生成器，每 yield 一块就立刻推给客户端，不等数据凑齐：

```python
from fastapi.responses import StreamingResponse

@app.get("/api/stream")
async def stream():
    async def gen():
        yield "第一块数据\n"
        await asyncio.sleep(1)    # 这1秒里客户端已经收到了第一块
        yield "第二块数据\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
```

- 不设 Content-Length，走 HTTP chunked 分块传输
- 背压友好：生成器惰性执行，网络发不动就暂停产出，不会堆内存
- 客户端断开时生成器被取消，可在 finally 里做清理
- 注意：生成器在事件循环里跑，别做 CPU 密集活，会卡住整个服务
- media_type="text/event-stream" + "data: xxx\n\n" 格式 = SSE 协议，前端用 EventSource 接收

**几个细节**

- 响应头一旦开始发送就改不了：StreamingResponse 的 headers 在第一个 chunk 发出前定型
- 文件下载优先 FileResponse（零内存拷贝 + 断点续传），数据还在产生中才用 StreamingResponse
- 三者的本质区别：**数据全部就绪才返回（JSON）vs 文件已存在（File）vs 数据边产生边发（Streaming）**

## 异常处理

对于客户端引发的错误返回一个错误响应

```python
from fastapi import FastAPI, Path, Query, HTTPException

@app.get("/id_num/{user_id}")
async def get_id_num(user_id: int):
    if user_id == 1:
        raise HTTPException(status_code=404, detail="用户id不存在")
    return {"message": f"用户id为{user_id}"}
```





## 中间件

中间件是一个函数，在每次请求进入fastAPI应用时都会执行。

![在这里插入图片描述](images/cf5ff0a30d766d22859aaace651906b5.png)

```python
from fastapi import Request, Response, FastAPI

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print("Middleware called")
    response = await call_next(request)
    print("Middleware ended")
    return response

@app.middleware("http")
async def add_process_time_header2(request: Request, call_next):
    print("Middleware2 called")
    response = await call_next(request)
    print("Middleware2 ended")
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}

#输出
INFO:     Application startup complete.
Middleware2 called
Middleware called
Middleware ended
Middleware2 ended
```

## 依赖注入

![image-20260318134851425](images/image-20260318134851425.png)

依赖性，是可以重复使用的组件。注入，FASTapi自动帮助你调用依赖性，并将`结果`注入到路径操作函数中。

**三步：创建依赖性（通用代码封装起来） 导入Depends   声明依赖性**

```python

#导入Depends
from fastapi import Depends


#创建依赖项
async def commen_func(
        skip:int = Query(0, ge=0, description="Number of items to skip"),
        limit:int = Query(100, ge=0, le=100, description="Number of items to limit")
):
    return {"skip": skip, "limit": limit}


#声明依赖性
@app.get("/items/{item_id}")
async def read_item(result = Depends(commen_func)):
    return result


```

