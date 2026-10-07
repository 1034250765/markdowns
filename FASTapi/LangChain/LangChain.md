## 目录

- **模型抽象与消息协议**
    
    - Chat Model、System/Human/AI/Tool Message
    - 基础调用、流式输出、结构化响应
- **提示词工程与结构化输出**
    
    - Prompt Template
    - `with_structured_output`
    - 再学习传统 Output Parser  
        现在很多场景优先使用模型原生结构化输出，不必一开始深入 Parser。
- **LCEL 表达式语言**
    
    - Runnable
    - 管道 `|`
    - `invoke`、`batch`、`stream`
    - `RunnablePassthrough`、分支和并行
- **工具绑定与调用**
    
    - 定义工具
    - `bind_tools`
    - Tool Call 消息
    - 多轮工具调用循环
- **RAG 核心闭环**
    
    - 文档加载与切分
    - Embedding 与向量库
    - Retriever
    - Context 拼接和答案生成
    - 引用、过滤、评估
- **最后补 Agent**
    
    - 把模型、工具、LCEL/RAG 组合起来
    - 再进入 LangGraph 的状态、节点、边和持久化



## **模型抽象与消息协议**

### chat_model

可以创建通用`init_chat_model` ，也可以创建ChatDeepSeek这种继承了的专用类。

|              | `ChatDeepSeek`             | `init_chat_model`                  |
| ------------ | -------------------------- | ---------------------------------- |
| 来源           | `langchain-deepseek` 包     | `langchain` 核心包                    |
| 类型提示         | 精确到 `ChatDeepSeek`，IDE 补全好 | 返回 `BaseChatModel`，补全弱             |
| 支持的 provider | 只有 DeepSeek                | 所有已装的集成包（openai/anthropic/ollama…） |
| 参数校验         | 构造时就报错                     | 运行时才报错                             |
| 动态换模型        | 要自己写 if/else               | 内置 `configurable_fields`           |
| 特有参数         | 完整支持                       | 透传 `**kwargs`，但拼错不报错               |


```python
# 两种写法都行
init_chat_model("deepseek-chat", model_provider="deepseek")
init_chat_model("deepseek:deepseek-chat")     # provider:model 格式


model = init_chat_model( "claude-sonnet-4-6", # Kwargs passed to the model: temperature=0.7, timeout=30, max_tokens=1000, max_retries=6, # Default; increase for unreliable networks )



from langchain_deepseek import ChatDeepSeek

  

llm = ChatDeepSeek(

    model=os.getenv("DeepSeekModel"),

    api_key=os.getenv("DeepSeekApiKey"),

    api_base=os.getenv("DeepSeekApiUrl"),

    temperature=0.7,

    max_retries=2,

    timeout=60,

)

llm


```



DeepSeek 的 API 是 OpenAI 兼容的，所以还有第三种写法，调试代理/自定义 base_url 时常用：

```python
from langchain_openai import ChatOpenAI
m = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key="...",
)


```


但它会丢掉 `ChatDeepSeek` 对 DeepSeek 特有字段（比如 reasoning 相关内容）的处理，能用前两种就别用这个。

装包：`pip install langchain-deepseek`（`init_chat_model` 内部也是动态 import 这个包，所以同样要装）。

**创建 ChatDeepSeek**

  

参数名说明（已核对 `ChatDeepSeek.model_fields`）：
  

| 参数 | 别名 | 说明 |

|------|------|------|

| `model` | `model_name` | 模型 ID |

| `api_key` | — | 密钥 |

| `api_base` | `base_url` | 接口地址 |

| `temperature` | — | 取值 `[0, 2]`，越大越发散 |

| `max_retries` | — | 网络失败自动重试次数 |

| `timeout` | `request_timeout` | 单次请求超时（秒） |


### 两种调用方式

- `invoke()` — 传字符串或消息列表，返回一条 `AIMessage`
- `stream()` — 逐块返回，适合打字机效果
- `HumanMessage`  用户提示词
- `SystemMessage` 系统提示词


```Python

resp = llm.invoke("用一句话介绍你自己")

print(resp.content)

print()

print("usage:", resp.additional_kwargs.get("reasoning_content"))


from langchain_core.messages import HumanMessage, SystemMessage

  

messages = [

    SystemMessage("你是一个代码补全助手。"),

    HumanMessage("扩散模型的工作原理是什么？"),

]

print(llm.invoke(messages).content)



for chunk in llm.stream(messages):

    print(chunk.content, end="", flush=True)


```


### 对比 init_model

```Python



from langchain.chat_models import init_chat_model

  

llm2 = init_chat_model(

    os.getenv("DeepSeekModel"),

    model_provider="deepseek",

    api_key=os.getenv("DeepSeekApiKey"),

    base_url=os.getenv("DeepSeekApiUrl"),  # 注意：这里是别名 base_url，不是 api_base

    temperature=0.7,

)

  

print("type      :", type(llm2).__name__)

print("isinstance:", isinstance(llm2, ChatDeepSeek))

print("reply     :", llm2.invoke("reply with exactly: OK").content)


# init_chat_model 独有的能力：运行时换模型，不用改代码

flexible = init_chat_model(

    os.getenv("DeepSeekModel"),

    model_provider="deepseek",

    api_key=os.getenv("DeepSeekApiKey"),

    base_url=os.getenv("DeepSeekApiUrl"),

    configurable_fields=("model", "temperature"),

)

  

print("默认    :", flexible.invoke("reply with exactly: A").content)

print(

    "换 V4-Pro:",

    flexible.invoke(

        "reply with exactly: B",

        config={"configurable": {"model": "deepseek-v4-pro"}},

    ).content,

)
```


### Message




### 模型调用


在 LangChain 中，模型调用（Invocation）是指通过特定方法触发大语言模型生成输出的过程。根据不同的应用场景和需求，LangChain 提供了几种核心的调用方式，主要是 invoke() 、stream() 和 batch() 方法，以及它们的异步版本 ainvoke() 、astream() 和abatch() ，下面将系统地介绍这些方法。

| 方法 | 特点 | 适用场景 |
|---|---|---|
| `invoke()` | 阻塞式，**一次性返回完整结果** | 问答、批处理任务、无需实时反馈的场景 |
| `ainvoke()` | 非阻塞式，提高系统吞吐量 | 高并发 Web 应用、IO 密集型任务 |
| `stream()` | 流式输出，**实时返回每个 token** | 聊天机器人、长文本生成、需要提升用户体验的交互应用 |
| `astream()` | 非阻塞式，提高系统吞吐量 | 高并发 Web 应用、IO 密集型任务 |
| `batch()` | **批量处理多个输入** | 高并发场景，需要同时处理大量请求 |
| `abatch()` | 非阻塞式，提高系统吞吐量 | 高并发 Web 应用、IO 密集型任务 |


invoke方法非常灵活，支持三种形式的输入：文本输入、字典列表、消息对象列表。

```python


## 文本输入

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

# 从.env文件中加载环境变量
load_dotenv(override=True)

CLOSEAI_API_KEY = os.getenv("CLOSEAI_API_KEY")
CLOSEAI_BASE_URL = os.getenv("CLOSEAI_BASE_URL")

model = init_chat_model(
    model="openai:gpt-5.4-mini",
    api_key=CLOSEAI_API_KEY,
    base_url=CLOSEAI_BASE_URL
)
# 向模型发送单条数据
prompt = "翻译成英文：你好世界"
response = model.invoke(prompt)

# 打印响应
print(response)
```


**字典列表**

```json

messages = [
    {"role": "system", "content": "系统提示"},
    {"role": "user", "content": "用户消息"},
    {"role": "assistant", "content": "AI回复"},  # 可选，用于对话历史
    {"role": "user", "content": "继续提问"}
]

```

角色说明：

| 角色        | 英文           | 作用                 | 示例                   |
| --------- | ------------ | ------------------ | -------------------- |
| system    | System       | 设定 AI 的行为、角色、规则    | "你是一个专业的 Python 导 师" |
| user      | Human/User   | 用户的输入/问题           | "什么是装饰器？"            |
| assistant | AI/Assistant | AI 的历史回复（用于对话上下 文） | "装饰器是一种设计模式..."      |


**消息对象列表**

| 消息类           | 对应字典格式                     | 作用    |
| ------------- | -------------------------- | ----- |
| SystemMessage | {"role": "system", ...}    | 系统提示  |
| HumanMessage  | {"role": "user", ...}      | 用户输入  |
| AIMessage     | {"role": "assistant", ...} | AI 回复 |


```python

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="你是一个 Python 专家"),
    HumanMessage(content="什么是生成器？"),
]

response = model.invoke(messages)
# print(response)

# 继续对话
messages.append(AIMessage(content=response.content))
messages.append(HumanMessage(content="能给个例子吗？"))

response1 = model.invoke(messages)
print(response1)

```

BaseMessage

```python

class BaseMessage(Serializable):
    content: str | list[str | dict[Any, Any]]
    additional_kwargs: dict[Any, Any] = Field(default_factory=dict)
    response_metadata: dict[Any, Any] = Field(default_factory=dict)
    type: str
    name: str | None = None
    id: str | None = Field(default=None, coerce_numbers_to_str=True)
    model_config = ConfigDict(extra="allow")
```




```




invoke 返回一个AIMessage对象，源码如下：

```python

class AIMessage(BaseMessage):

  

    tool_calls: list[ToolCall] = Field(default_factory=list)

    invalid_tool_calls: list[InvalidToolCall] = Field(default_factory=list)

    usage_metadata: UsageMetadata | None = None


    type: Literal["ai"] = "ai"


    @overload

    def __init__(

        self,

        content: str | list[str | dict[Any, Any]],

        **kwargs: Any,

    ) -> None: ...

  

    @overload

    def __init__(

        self,

        content: str | list[str | dict[Any, Any]] | None = None,

        content_blocks: list[types.ContentBlock] | None = None,

        **kwargs: Any,

    ) -> None: ...

  

    def __init__(

        self,

        content: str | list[str | dict[Any, Any]] | None = None,

        content_blocks: list[types.ContentBlock] | None = None,

        **kwargs: Any,

    ) -> None:


        if content_blocks is not None:

            # If there are tool calls in content_blocks, but not in tool_calls, add them

            content_tool_calls = [

                block for block in content_blocks if block.get("type") == "tool_call"

            ]

            if content_tool_calls and "tool_calls" not in kwargs:

                kwargs["tool_calls"] = content_tool_calls

  

            super().__init__(

                content=cast("list[str | dict[Any, Any]]", content_blocks),

                **kwargs,

            )

        else:

            super().__init__(content=content, **kwargs)
```

**invoke 和 stream 有什么区别？**

- invoke() ：同步调用，在模型输出完成后**一次性获取响应**，对于输出文本很长的场景，用户体验不好。
- stream() ：流式调用，**实时返回响应片段**。调用后，返回一个迭代器(iterator) ，可以通过循环来实时处理每一个新生成的chunk内容块。

注意：流式输出依赖于模型供应商对于流式输出的支持。

```python

```python
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

# 从.env文件中加载环境变量
load_dotenv(override=True)

CLOSEAI_API_KEY = os.getenv("CLOSEAI_API_KEY")
CLOSEAI_BASE_URL = os.getenv("CLOSEAI_BASE_URL")

model = init_chat_model(
    model="gpt-5.4-mini",
    api_key=CLOSEAI_API_KEY,
    base_url=CLOSEAI_BASE_URL
)

for chunk in model.stream("写一首七言律诗，总结大模型的发展"):
    print(chunk.text, end="", flush=True) # 逐token输出

```

在调用模型时（如使用 invoke(), ainvoke(), stream(),batch()等方法时），我们可以传入config参数。config参数：**允许在调用模型时，动态地配置和控制模型的行为**，而无需在初始化时就固定所有参数，这为应用带来了极大的灵活性和可维护性。

### 为什么需要结构化响应

LLM 默认输出的是自然语言文本。如果下游业务需要把数据存入数据库、传递给 API、触发特定工作流或供前端组件渲染，非结构化文本通常面临以下痛点：

- **难以解析**：模型可能会附带客套话（如 "Here is your JSON:"）、Markdown 代码块（` ```json `）或错乱的标点。
    
- **字段缺失或类型错误**：数值可能变成字符串，布尔值可能变成单词，关键键名拼写飘忽不定。
    
- **稳定性差**：纯 Prompt 约束（"请只输出 JSON"）无法百分之百保证格式合法性。
    

结构化响应将自然语言直接转换成强类型、可预测、易验证的程序对象。


**LangChain 中的核心实现方式**

#### 1. 首选方案：`.with_structured_output()`

现代大模型（如 OpenAI、Anthropic、Google Gemini、Mistral 等）大多原生支持 **Tool Calling（工具调用）** 或 **JSON Mode**。LangChain 在 `ChatModel` 上提供了一个通用的 `.with_structured_output()` 方法，这是目前官方最推荐的实践。

它支持传入：

- **Pydantic Model**（推荐，自带数据校验）
    
- **TypedDict / Dataclass**
    
- **JSON Schema**
    

**代码示例（基于 Pydantic）：**

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# 1. 定义期望的响应结构
class UserProfile(BaseModel):
    name: str = Field(description="用户姓名")
    age: int = Field(description="用户年龄")
    interests: list[str] = Field(description="用户的兴趣爱好列表")

# 2. 绑定结构到模型
llm = ChatOpenAI(model="gpt-4o", temperature=0)
structured_llm = llm.with_structured_output(UserProfile)

# 3. 调用并直接获得 Pydantic 对象
result = structured_llm.invoke("张三今年28岁，平时喜欢摄影、徒步和看科幻小说。")

print(type(result))      # <class '__main__.UserProfile'>
print(result.name)        # 张三
print(result.age)         # 28
print(result.interests)   # ['摄影', '徒步', '科幻小说']


```