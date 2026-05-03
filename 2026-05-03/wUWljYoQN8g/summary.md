# 40 分钟讲透 Context Engineering

## 视频信息

- 标题：Everything You Need to Know About Context Engineering in 40 Minutes | Ravi Mehta
- 链接：<https://youtu.be/wUWljYoQN8g>
- 嘉宾：Ravi Mehta
- 主持人：Peter Yang

## 核心结论

- Prompt engineering 没有消失，但已经降级为 context engineering 的一个子集。
- 真正高质量的 AI 原型，不靠一句聪明 prompt，而靠完整上下文系统。
- Ravi 提出的三层框架非常实用：**functional context、visual context、data context**。
- 原型的目标不是“做出来”，而是**帮助团队做决策、拿到真实反馈**。
- MCP / API / 外部工具也是 context 的一部分，决定原型能否从“像”走向“真”。

## 关键观点

### 1. 为什么很多 AI 原型看起来像 AI slop

因为多数人只给了一个 quick prompt 或 mini spec，却没有提供：

- 清晰的功能上下文
- 可参考的视觉上下文
- 独立、真实、可替换的数据上下文
- 必要的外部工具能力

结果就是页面能跑，但质感、结构、可信度都很弱。

### 2. Context engineering 的定义

Ravi 的定义：

> 设计并构建系统，为 AI 模型提供完成任务所需的正确信息与工具。

重点不是“和模型聊天”，而是“为模型配置工作环境”。

### 3. 三层上下文框架

#### Functional context
- 说明产品要做什么
- 包括功能、交互、约束和目标

#### Visual context
- 告诉模型界面应该长什么样
- 可以来自截图、线框图、Figma、风格参考

#### Data context
- 用 JSON 等结构化格式定义真实数据
- 让原型不再依赖 dummy data
- 也让界面与数据层解耦，更容易替换与迭代

### 4. Full-stack prompt 的真正含义

不是写更长的 prompt，而是把：

- functional
- visual
- data

三层上下文编排成一个结构清晰、可被模型理解的输入包。

### 5. MCP server 的启发

Ravi 为音乐原型补了一个自定义 MCP server，用来抓取专辑封面。

这说明：

- 工具能力本身就是 context 的一部分
- 模型差的那一口气，有时不是 prompt，而是 API / tool access

### 6. PRD 与 prototype 的关系变了

旧流程强调：PRD → wireframe → design → MVP。

Ravi 的判断是：今天不必拘泥于这个严格线性顺序。

- 有时 PRD 在 prototype 前面
- 有时 prototype 先跑，再反过来完善 PRD

关键是：**你想回答什么问题、验证什么假设。**

## 给 AI 产品实践者的 5 条建议

1. 别只优化 prompt，先补全 context。
2. 把数据层独立出来，优先使用结构化 JSON。
3. 给视觉参考，不要让模型自由发挥审美。
4. 把 prototype 当决策工具，而不是演示玩具。
5. 学一点 MCP / API / 工具编排，收益非常高。

## 一句话总结

**Prompt 是一句话，context 是整个工作台。**

谁更会组织上下文，谁就更容易做出不像 AI slop 的 AI 产品。
