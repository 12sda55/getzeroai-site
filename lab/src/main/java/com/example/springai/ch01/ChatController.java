package com.example.springai.ch01;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

/**
 * 第 1 章 · 对外 HTTP 接口。
 *
 * Controller 只做三件事：接参数 → 调 Service → 返回结果。
 * 不要在 Controller 里写业务逻辑，也不要直接注入 ChatClient。
 *
 * 用 curl 验证（应用启动后）：
 *   同步：curl -X POST http://localhost:8080/api/v1/chat/ask ^
 *             -H "Content-Type: application/json" ^
 *             -d "{\"question\":\"用一句话介绍 Spring AI\"}"
 *   流式：curl -N -X POST http://localhost:8080/api/v1/chat/stream ^
 *             -H "Content-Type: application/json" ^
 *             -d "{\"question\":\"用三句话介绍 Spring AI\"}"
 *         （-N 表示关闭缓冲，能看到一个字一个字往外蹦）
 */
@RestController
@RequestMapping("/api/v1/chat")
public class ChatController {

    private final HelloAiService service;

    // 构造器注入（推荐）：字段少一个 @Autowired，还便于单元测试时手工构造
    public ChatController(HelloAiService service) {
        this.service = service;
    }

    /** 同步：适合后台任务、脚本调用 */
    @PostMapping("/ask")
    public String ask(@RequestBody AskRequest req) {
        return service.ask(req.question());
    }

    /**
     * 流式：produces 必须是 text/event-stream（SSE 协议），
     * 前端用 EventSource 或 fetch + ReadableStream 接收。
     */
    @PostMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> stream(@RequestBody AskRequest req) {
        return service.askStream(req.question());
    }

    /** 用 record 接收请求体，比 Map 更安全（字段名编译期就能检查） */
    public record AskRequest(String question) {}
}
