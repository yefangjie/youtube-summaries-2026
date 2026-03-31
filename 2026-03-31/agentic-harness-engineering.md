# 从Anthropic到OpenAI：Agentic Harness Engineering 正在重塑AI开发

在当前的AI工程圈，一个名为 **Agentic Harness Engineering** 的概念正在迅速成为年度流行语。从单纯的 Prompt Engineering 到 RAG（检索增强），再到自主智能体（Agent），AI的应用落地遇到了一个棘手的瓶颈：如何管理一个“绝顶聪明但缺乏工作经验且容易遗忘”的AI？

Mitchell Hashimoto 给出了一个精准的比喻：如果 Agent 是引擎，那么 Harness 就是底盘、方向盘、刹车和导航系统。Harness Engineering 的核心，不再是教模型怎么写代码，而是教系统怎么管理模型写代码的过程。本文将带你深度解析 Anthropic、OpenAI 和 Google 这三大巨头的内部实践。

##  开场：Agentic Harness Engineering 的崛起

大家好，欢迎来到本期视频。我是 Tommy。最近在 AI 工程圈，有一个词正在迅速成为年度流行语——Agentic Harness Engineering。

如果你一直关注大型语言模型的应用，你肯定知道从单纯的 Prompt Engineering 到 RAG 检索增强，再到现在的 Agent 自主智能体，这已经是共识的发展路径了。但 Agent 真正落地的时候，大家发现了一个很尴尬的问题。

就像你雇了一个绝顶聪明、但没有工作经验、甚至有点健忘的实习生。你把任务交给他，他一开始干得热火朝天，结果中途遇到一个报错，他就卡住了，或者开始瞎编，更惨的是，第二天他把昨天的工作全忘了。

这就是为什么现在各大厂都在谈论 Harness Engineering。

Mitchell Hashimoto 在他的博客里给了一个很好的定义。他说，如果 Agent 是引擎，Harness 就是底盘、方向盘、刹车和导航系统。

Harness Engineering 的核心，不再是教模型怎么写代码，而是教系统怎么管理模型写代码的过程。今天我们就来深度扒一扒 Anthropic、OpenAI 和 Google 这三大巨头，看看他们是怎么把这群“聪明但缺乏常识的实习生”管得服服帖帖的。

##  Anthropic 的实践：双 Agent 架构与外部记忆

我们先来看 Anthropic 的案例。他们在 2026 年初分享了一个非常硬核的内部实践——用 Claude 3.5 Sonnet 开发他们自己的前端框架组件。

Anthropic 遇到的最大痛点是“上下文迷失”。一个复杂的开发任务，往往需要横跨几十个文件，来回修改、测试、排错。传统的单 Agent 模式，跑着跑着就忘了自己最初的目标是什么，或者在处理长尾 Bug 时陷入死循环。

他们的解法是什么？**双 Agent 架构（或者叫初始化与执行分离）。**

初始化 Agent 只在第一个 session 运行，负责建立环境：创建初始化脚本、写入一个进度日志文件、建立 git 基线，然后——这是关键——把用户的高层级指令扩展成数百条具体的、可测试的功能需求清单，以 JSON 格式存下来。 

编码 Agent 在后续 session 中逐个功能推进，每次启动先确认当前位置、读进度文件、审查功能清单、跑已有测试。 

这里有一个很重要的设计思想——外部制品成为 Agent 记忆。进度文件、git 历史、结构化需求清单跨 session 持久化，每个 Agent session 在动手之前先从这些制品重建上下文。 

技术上还有个细节值得注意——Anthropic 自己说了，这两个 Agent 其实并不是真正独立的 Agent，他们共享相同的系统提示、工具集和整体 harness，唯一区别只是初始用户提示不同。 

换句话说，仅通过提示工程就能在单一 harness 内创造专门化行为。 

然后到了 2026 年 3 月，方案演进成了三 Agent 架构——planner 负责扩展需求、generator 负责实现、evaluator 负责用 Playwright 这类工具做交互式验证和打分。 

这里面最有意思的发现是什么？是评估器分离这件事。Anthropic 发现，当你让模型评估自己的工作时，它会倾向于自信地表扬自己的作品——即使在人类看来质量明显平庸。 

这不是哪个模型的问题，这是自评估的系统性缺陷。他们的结论是：工程化一个独立的严格评估器 Agent，远比教会生成器 Agent 自我批评要容易得多。 

说到这里我很好奇——你们自己用 Agent 做开发的时候，有没有遇到过 Agent 自信满满告诉你“搞定了”，结果一检查全是半成品的经历？弹幕里扣个 1 让我看看。 

另一个关键发现跟模型迭代有关。他们早期 harness 用的是 Sonnet 4.5，这个模型有一种很明显的“上下文焦虑”倾向——随着上下文增长，模型会变得不稳定，所以 harness 里设计了上下文重置机制。 

但换成 Opus 4.5 之后，模型自行消除了这个行为，上下文重置机制就变得不再必要了。这说明什么？说明 harness 不是越复杂越好，它必须跟模型当前的能力边界相匹配。 

模型强了，有些 harness 模块反而应该撤掉。 

##  OpenAI 的实践：百万行代码实验

再看 OpenAI。OpenAI 的案例更具传播力，因为他们给出了非常具体的数据。 

2025 年 8 月开始，一个最初只有三个人、后来扩展到七个人的工程团队，用 GPT 5 驱动的 Codex Agent，在大约五个月里生成了约百万行代码，合并了约一千五百个 PR，构建了一个有内部日活用户和外部 alpha 测试者的生产级产品。 

团队人均日吞吐量大约 3.5 个 PR，而且随着团队扩大吞吐量反而上升了。 

他们还给自己加了一个极端约束——零行手写代码。所有应用逻辑、测试、CI、文档、可观测性和内部工具全部由 Codex 生成。 

他们坦承构建速度大约是手写的十分之一，但认为这是一种可接受的换取。 

Martin Fowler 网站上的 Boeckeler 对 OpenAI 的 harness 做了一个很精炼的归纳——三大支柱。 

第一是 Context Engineering，持续增强代码库中的知识库，加上 Agent 对可观测性数据和浏览器的动态访问。 

第二是架构约束，不只是靠 Agent 自觉遵守，而是用确定性的自定义 linter 和结构测试来执行。 

第三，这个很有意思——叫“垃圾回收”，定期运行后台 Agent 扫描文档不一致和架构违规，对抗系统的熵增。 

OpenAI 团队发现的一个核心模式非常值得记住——当 Agent 遇到困难时，不要“更努力地尝试”，而是反问“缺少什么能力？怎么让这个能力对 Agent 来说既可读又可执行？”然后让 Codex 自己编写修复代码。这形成了一个 harness 自我改进的闭环。 

但这里我必须加一个诚实度提醒。Boeckeler 在她的分析里明确指出，OpenAI 在呈现这个案例时“有既得利益让我们相信 AI 可维护代码”。 

而且她还发现了一个有趣的细节——那篇文章标题虽然叫 Harness Engineering，但正文里 harness 这个词只出现了一次。这个标题很可能是受 Mitchell Hashimoto 那篇博客启发后加上去的。 

所以对这个案例，该学的学，该存疑的也得存疑。 

##  Google DeepMind 的实践：Aletheia

然后是 Google DeepMind。Google 在 harness 这件事上没有像 Anthropic 和 OpenAI 那样发一篇专门的方法论文章，但他们用产品说话了。 

2026 年 2 月，DeepMind 发布了 Aletheia——一个面向数学研究的自主 Agent。 

它的核心架构恰好就是一个三组件的 agentic harness：Generator 负责提出候选解法和证明策略，Verifier 用自然语言检查逻辑缺陷和幻觉，Reviser 负责修正验证器发现的错误。三个组件循环迭代，直到输出通过验证。 

##  行业共识：生成-评估分离

注意到了吗？Generator、Verifier、Reviser——这跟 Anthropic 的 planner、generator、evaluator 三 Agent 架构高度对应。 

两家公司独立走到了同一个设计模式上。这不是巧合，这说明“生成-评估分离”正在成为 Agent harness 设计的行业共识。 

Aletheia 的成果也很亮眼——在 IMO-Proof Bench Advanced 上达到百分之九十五点一的准确率，自主解决了 Erdos 猜想数据库中四个此前未被解决的开放问题。 

但也有批判性报道指出，它在更广泛的问题集上错了百分之六十八点五。这恰好说明了 harness 的一个特点——在特定场景下可以非常强大，但泛化能力仍然受限于 harness 的设计边界。 

##  Google 的工具与 Gemini 3 的状态持久性

Google 在工具层面也有动作。他们的 Agent Development Kit——简称 ADK——是一个开源的 Agent 框架，定位类似 Anthropic 的 Claude Agent SDK。 

里面内置了 evaluation harness 做场景驱动测试，还有 Agent Starter Pack 提供生产级脚手架，包括 CI/CD 管道、测试框架和监控配置。2026 年 3 月发布的 ADK Python 2.0 Alpha 还加入了图式工作流编排。 

另外还有一个技术细节值得一提。Gemini 3 在 2026 年 3 月引入了一个叫 Thought Signatures 的机制——模型在调用工具之前，会生成一个加密的推理状态表示，传回对话历史之后可以恢复精确的推理链路。 

这本质上是在模型层面解决跨步骤的状态持续性问题。Anthropic 用的是 harness 层面的外部制品——进度文件、git 历史来保持记忆，Google 则尝试在模型内部解决同样的问题。两条路线，值得持续观察哪条更有效。 

##  Vercel 的经验：少即是多

除了三大巨头，还有几个案例非常值得聊。Vercel 提供了一个完全反直觉的经验。 

他们最初给 Agent 配了一个非常全面的工具库——搜索、代码、文件、API 工具全都有——结果效果很差。Agent 变得困惑，进行冗余调用，执行不必要的步骤。 

然后 Vercel 做了一件看起来倒退的事——他们移除了百分之八十的工具。结果反而获得了更好的效果：更少的步骤、更少的 token 消耗、更快的响应、更高的成功率。 

这件事告诉我们一个非常重要的设计原则——约束 Agent 的解决空间，反而能提升它的表现。 

Boeckeler 把这个洞察提炼到了更深的层次：为了获得更多 AI 自主性，运行时环境反而需要更多约束，而非更少护栏。这跟传统软件开发里“给工程师更多自由度”的理念完全相反。 

##  Stripe 的实践：环境与工具对齐


---
*本文基于 YouTube IBM Technology 频道关于 Agentic Harness Engineering 的技术解析整理而成。*
