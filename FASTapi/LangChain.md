

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

