

Pydantic 是一个 Python 数据校验库，它的核心思想是：**用 Python 类型注解定义数据结构，Pydantic 自动负责校验和转换**。在 FastAPI 中，Pydantic 主要用于：

|用途|说明|
|---|---|
|请求体校验|自动校验客户端发送的 JSON 数据是否符合模型定义|
|响应体序列化|将模型数据自动转换为 JSON 响应|
|自动文档|模型的字段、类型和校验规则自动出现在 API 文档中|
|编辑器支持|模型属性在编辑器中获得完整的自动补全|

创建一个继承 `BaseModel` 的类，使用 Python 标准类型声明字段：

```python

from pydantic import BaseModel


class Item(BaseModel):
    name: str               # 必填：商品名称
    description: str | None = None  # 可选：商品描述
    price: float            # 必填：商品价格
    tax: float | None = None        # 可选：税费

```

字段是否必填取决于是否有默认值：

|字段|声明方式|是否必填|
|---|---|---|
|`name`|`name: str`|必填|
|`description`|`description: str \| None = None`|可选|
|`price`|`price: float`|必填|
|`tax`|`tax: float \| None = None`|可选|
### 作为请求体

最常见的用法是将模型声明为路径操作函数的参数：

```python

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    # FastAPI 自动校验请求体，校验通过后赋值给 item 参数
    return item
```

**`BaseModel` 是 Pydantic 的模型基类：一个普通 Python 类，但它的元类是 `ModelMetaclass`。** 这使得任何 `class X(BaseModel)` 在**定义的那一刻**就被自动加工 —— 读注解、编译成 Rust 校验器、挂上一整套校验/序列化/Schema 方法。                    **运行时验证**

你可以把它理解成：**一个带类型契约、会自动校验和强转、还会自己生成文档的 `dict`。**
可以冻结属性的值，不大于不小于，赋予列表默认值。








## Optional

在主流编程语言中，`Optional` 主要出现在 **Java**、**C++** 和 **Python** 中，核心目的都是为了**优雅地处理可能为 null / None / 空的值，避免空指针异常**。


```python
from typing import Optional

# 表示参数 name 可以是 str，也可以是 None
def greet(name: Optional[str] = None) -> str:
    if name is None:
        return "Hello, Guest"
    return f"Hello, {name}"

# Python 3.10+ 更推荐使用管道符写法（无需导入 Optional）
def greet_new(name: str | None = None) -> str:
    return f"Hello, {name or 'Guest'}"

```