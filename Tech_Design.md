幸福设计系统 Tech Design
1. 技术栈选择
前端架构采用跨端编译方案。结合常见技术生态，选用 uni-app 或 Taro。此方案在前期可快速编译为 H5 网页进行业务验证，后期仅需调整少量平台层代码即可生成微信小程序。图表渲染采用 ECharts，在不同终端引入对应的兼容组件即可。
后端服务采用 Python 语言搭配 FastAPI 框架。Python 具备处理大语言模型 API 的先天优势。FastAPI 支持异步编程，能够稳定承载流式对话的并发请求。
数据存储层面，关系型数据库选用 PostgreSQL，负责账户信息、日记文本以及量化分数的持久化记录。缓存组件选用 Redis，用于处理多轮对话过程中的临时上下文和会话状态，降低数据库压力并提升交互响应速度。
2. 项目结构
代码组织遵循前后端分离原则，典型的结构设计如下：
/happiness-design-system
├── /frontend            (前端跨端工程)
│   ├── /src
│   │   ├── /components  (公共组件：图表、对话气泡)
│   │   ├── /pages       (核心页面：对话复盘、日记展示、历史数据)
│   │   ├── /services    (后端 API 交互与请求封装)
│   │   └── /utils       (格式化工具、状态管理)
│   └── package.json
├── /backend             (后端 FastAPI 工程)
│   ├── /app
│   │   ├── /api         (路由定义：对话接口、日记拉取)
│   │   ├── /core        (系统配置：大模型参数、数据库连接)
│   │   ├── /models      (ORM 数据映射模型)
│   │   ├── /services    (业务逻辑：提示词拼装、分数计算)
│   │   └── main.py      (应用主入口)
│   └── requirements.txt
└── /docs                (产品需求与技术架构文档)
3. 数据模型
核心数据结构需要涵盖用户属性、每日复盘总览以及具体的维度切片。
Users 用户表
    user_id (主键)
    username
    created_at
Daily_Journals 日记总表
    journal_id (主键)
    user_id (外键)
    record_date (记录日期)
    total_score (当日幸福总分)
    ai_summary (AI 行为总结)
    intervention_advice (干预建议)
Element_Scores 维度评分明细表
    score_id (主键)
    journal_id (外键)
    element_name (要素名称：意义、意志等)
    score (1到10分)
    behavior_fact (客观行为事实记录)
Chat_Context 对话上下文状态 (存储于 Redis)
    session_id
    user_id
    current_element (当前处于哪个维度的探查)
    messages (本轮对话历史记录)
4. 关键技术点
大语言模型上下文状态控制
多轮开放式对话容易导致大模型偏离预设的八要素流程。需要在后端代码中维护一个状态机，准确记录当前进行到哪一个要素的提问。每次向 LLM 发起请求时，需动态将当前所处维度的状态指令注入系统提示词中，强制模型按业务既定顺序推进。
流式对话接口实现
传统的 HTTP 等待机制会导致 AI 生成长文本时产生明显的卡顿感。必须采用 Server-Sent Events 或 WebSocket 技术实现后端的流式文本输出。前端接收到字节流后实时渲染对话内容，降低用户的等待耗时。
结构化数据提取与解析
模型在多轮对话结束后需要生成结构化的分数和行为记录存入数据库。由于 LLM 输出的不稳定性，需在最后一次请求中强制要求模型以 JSON 格式输出数据。后端需要配置健全的校验和解析机制，处理字段缺失或格式错误的情况。
前端图表跨端适配
ECharts 在 H5 环境和微信小程序环境下的底层渲染机制存在差异。开发阶段需要封装适配器，依据当前的运行环境动态加载对应依赖，保障数据趋势折线图和雷达图在不同终端上的显示效果一致。
