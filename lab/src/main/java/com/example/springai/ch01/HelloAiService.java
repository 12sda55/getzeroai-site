package com.example.springai.ch01;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

/**
 * 第 1 章 · 推荐的日常写法：通过 ChatClient 调用。
 *
 * ChatClient 和 ChatModel 的关系：
 *   - ChatModel 是"一次性调用"的底层接口（上一节 ChatModelBasics 演示的）
 *   - ChatClient 是高层封装：链式 API + 自动带上全局系统提示 + Advisor 链
 * 业务代码 95% 的情况只面向 ChatClient 写。
 */
@Service
public class HelloAiService {

    private final ChatClient chatClient;

    public HelloAiService(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    /** 最小可用：一句话进，一句话出 */
    public String ask(String question) {
        return chatClient.prompt()      // ① 开启一次请求构建
                .user(question)         // ② 设置用户消息（也可 .system(...) 覆盖默认）
                .call()                 // ③ 同步执行：阻塞等待完整结果
                .content();             // ④ 取出纯文本内容
    }

    /** 流式：一个字一个字往回推，前端体验好，适合聊天框 */
    public Flux<String> askStream(String question) {
        return chatClient.prompt()
                .user(question)
                .stream()               // ③' 换成 stream()，返回 Flux<String>
                .content();
    }

    /** 想看完整响应对象（含 Token 用量），用 chatResponse() 而不是 content() */
    public String askWithUsage(String question) {
        var response = chatClient.prompt()
                .user(question)
                .call()
                .chatResponse();        // ④' 拿到 ChatResponse
        var usage = response.getMetadata().getUsage();
        return "用量：" + usage.getTotalTokens() + " tokens\n"
                + response.getResult().getOutput().getText();
    }
}
