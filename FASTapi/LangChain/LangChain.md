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