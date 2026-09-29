# springai-lab —— 《Spring AI 2.0 学习指南》第 1 章配套示例

与教程站点 `http://www.getzeroai.xyz/springai/ch01.html` 的代码**逐字一致**，
每一条注释都对应教程里的一句讲解，可以对照着读。

## 版本基准

| 组件 | 版本 | 说明 |
|---|---|---|
| Spring Boot | 4.1.1 | Initializr 当前默认；Boot 3.x 不兼容，不可混用 |
| Spring AI | 2.0.1 | 由 `spring-ai-bom` 统一管版本 |
| Java | 17 | Spring AI 2.0 硬性底线 |
| Maven | 3.9.16 | 已装在 `D:/bc/apache-maven-3.9.16`；Boot 4 插件要求 ≥ 3.6.3，旧的 3.6.1 不够 |

## 如何运行

1. **配密钥**（Windows PowerShell）：
   ```powershell
   setx OPENAI_API_KEY "sk-你的密钥"
   # 配完要重开终端才生效
   ```
   密钥去 DeepSeek（默认）或智谱等平台申请，**不要写进任何文件**。

2. **编译并启动**（项目根目录）：
   ```bash
   mvn spring-boot:run
   ```
   看到类似 `Tomcat started on port 8080` 即启动成功。

3. **验证**：
   ```bash
   # 同步接口：等完整回答
   curl -X POST http://localhost:8080/api/v1/chat/ask \
        -H "Content-Type: application/json" \
        -d "{\"question\":\"用一句话介绍 Spring AI\"}"

   # 流式接口：一个字一个字往外蹦（SSE）
   curl -N -X POST http://localhost:8080/api/v1/chat/stream \
        -H "Content-Type: application/json" \
        -d "{\"question\":\"用三句话介绍 Spring AI\"}"
   ```

## 工程结构（按章节分包，后续每章一个包）

```
lab/
├── pom.xml                                  Maven 依赖清单（含大量注释）
└── src/main/
    ├── java/com/example/springai/
    │   ├── SpringaiLabApplication.java      启动类
    │   ├── common/                          全局配置（跨章节共用）
    │   │   └── ChatClientConfig.java        全局 ChatClient（默认系统提示 + 日志 Advisor）
    │   └── ch01/                            第 1 章：第一次调用大模型
    │       ├── ChatModelBasics.java         底层 ChatModel：看清消息列表的本质
    │       ├── HelloAiService.java          高层 ChatClient：日常推荐写法
    │       └── ChatController.java          HTTP 接口（同步 + SSE 流式）
    └── resources/application.yml            模型 / 超时 / 日志配置（换厂商只改这里）
```

## 常见问题

- **启动就报 401**：环境变量没生效，重开终端再启动；或密钥填错平台（密钥要和 base-url 匹配）。
- **换智谱**：`application.yml` 里把 `base-url` 改为 `https://open.bigmodel.cn/api/paas/v4`、`model` 改为 `glm-4-plus`，代码不动。
- **想看发给模型的请求体**：`application.yml` 里 `org.springframework.ai.chat.client: debug` 已默认打开，控制台直接看。
