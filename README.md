# Spring AI 2.0 学习指南

配套《Spring AI 框架与企业级智能应用开发实践 V2.0》的**自学 / 教学站点**。

面向已掌握 Spring Boot 基础的在校学生与开发者，以 **Spring AI 2.0** 为核心，
按 11 个章节梳理学习路径，每一章都包含：**要学什么 → 环境怎么配 → 代码怎么写 → 为什么这么写 → 跑起来看到什么 → 踩坑怎么排**。

所有代码示例均可直接复制到 IDEA 运行，不是伪代码。

---

## 快速开始

本站点是纯静态站点，**无需构建、无后端依赖**：

```bash
# 方式一：用 Python 起本地服务（推荐，避免 file:// 的脚本限制）
cd springai-study-guide
python -m http.server 8000
# 浏览器打开 http://localhost:8000

# 方式二：直接双击 index.html（部分浏览器会限制本地脚本加载）
```

在线阅读：见仓库部署地址，或参考 [`springai-study-guide/DEPLOY.md`](springai-study-guide/DEPLOY.md)。

---

## 目录结构

```
.
├── .gitignore
├── README.md
└── springai-study-guide/
    ├── index.html            总览 · 11 章学习路线 · 完整环境准备
    ├── ch01.html             Spring AI 入门
    ├── ch02.html             提示词与对话
    ├── ch03.html             结构化输出与 Advisors
    ├── ch04.html             嵌入模型与向量数据库
    ├── ch05.html             RAG
    ├── ch06.html             记忆与多模型
    ├── ch07.html             工具调用
    ├── ch08.html             MCP
    ├── ch09.html             智能体
    ├── ch10.html             可观测性与评估
    ├── ch11.html             综合项目：企业知识问答 + 工单辅助系统
    ├── appendix.html         速查手册 / 异常排查表 / 术语表
    ├── DEPLOY.md             部署说明（四种托管方式 + 上线自检清单）
    └── assets/
        ├── style.css
        └── app.js
```

---

## 学习路径

11 个章节不是并列关系，而是**层层叠加**的能力：

| 阶段 | 章节 | 目标 |
|---|---|---|
| 一 · 打通「能说」 | 1 – 3 | 从 Hello AI 到「输入可控、输出是结构化对象」 |
| 二 · 接上「知识」 | 4 – 5 | 向量化 → 建库建索引 → RAG 全链路 + 引用溯源 |
| 三 · 装上「记忆与手脚」 | 6 – 8 | 会话隔离、模型路由与降级、工具调用、MCP |
| 四 · 变成「系统」 | 9 – 11 | Agent 循环与人工确认、可观测性与评估、端到端交付 |

每章统一结构：

> 学习目标卡 → 概念详解 → 依赖与配置 → **逐行注释的代码解析** → 可运行示例 →
> **curl 验证命令 + 期望输出** → 排错对照表 → 可折叠自测题 → 验收标准

---

## 技术栈

- JDK 21（Spring AI 2.0 的硬性底线是 Java 17）· **Spring Boot 4.1.x** · **Spring AI 2.0.1** · Maven 3.6.3+
- MySQL 8 · Redis 7 · PostgreSQL 16 + pgvector · Milvus
- Docker / Docker Compose · Micrometer · OpenTelemetry · Zipkin
- 兼容 OpenAI 协议的模型服务（DeepSeek / 通义千问 / 智谱…）· Ollama 本地模型 · MCP Server

---

## 说明

- 全部代码以 **Spring AI 2.0.1**（2.0.0 GA：2026-06-12 / 2.0.1：2026-08-21）为基准编写，
  底座为 **Spring Boot 4.1.x + Spring Framework 7.0**。
- ⚠️ **Spring AI 2.0 是一次架构级重构，与 Spring Boot 3.x 不兼容**，不能混用。
  从 1.x 迁移的重点变化：工具调用循环上移为 `ToolCallingAdvisor`、
  `internalToolExecutionEnabled` 被删除、记忆的 `conversationId` 变为必填、
  配置移除了 `.options` 段、`PromptChatMemoryAdvisor` 被移除。
- 学习过程中遇到 API 名称不一致时，建议依次查：
  ① [2.0 升级说明](https://docs.spring.io/spring-ai/reference/2.0/upgrade-notes.html)（列全了破坏性变更）→
  ② [Spring AI 官方文档](https://docs.spring.io/spring-ai/reference/) →
  ③ IDE 中 `Ctrl+Alt+B` 看接口实现。

---

## 许可与使用

本仓库内容供学习、教学使用。文中引用的第三方项目与文档版权归各自所有者。
