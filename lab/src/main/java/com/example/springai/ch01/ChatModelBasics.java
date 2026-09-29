package com.example.springai.ch01;

import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * 第 1 章 · 最底层的调用方式：只用 ChatModel 接口。
 * 目的：看清一次对话请求到底由哪些部分组成。
 *
 * 学习顺序建议：先读懂本类（消息列表的本质），
 * 再看 HelloAiService（ChatClient 高层封装），层次感就出来了。
 */
@Component
public class ChatModelBasics {

    // 构造器注入。这个 bean 由 spring-ai-starter-model-openai 自动装配，
    // 类型实际是 OpenAiChatModel，但我们只依赖抽象接口，方便日后替换/测试打桩。
    private final ChatModel chatModel;

    public ChatModelBasics(ChatModel chatModel) {
        this.chatModel = chatModel;
    }

    /**
     * 最简单的调用：只传一句用户话。
     * 内部会自动包成一个只含 UserMessage 的 Prompt。
     */
    public String simple(String userText) {
        // call(String) 是 ChatModel 的便捷方法，等价于 new Prompt(userText)
        return chatModel.call(userText);
    }

    /**
     * 带系统提示 + 用户消息的标准写法。
     * 这是理解"消息列表"最直观的例子。
     */
    public String withSystemPrompt(String userText) {
        // SystemMessage：设定角色与规则，模型会当作最高优先级的背景指令
        SystemMessage system = new SystemMessage(
                "你是一名严谨的企业知识库助手，回答必须简洁，不确定时明确说不知道，禁止编造。");
        // UserMessage：用户这一轮真正说的话
        UserMessage user = new UserMessage(userText);

        // Prompt 的本质 = 有序的消息列表（+ 可选的模型参数）
        Prompt prompt = new Prompt(List.of(system, user));

        // call 返回的是 ChatResponse，里面不止有文本，还有元数据
        ChatResponse response = chatModel.call(prompt);

        // 逐层取值：response -> generation -> output(AssistantMessage) -> text
        return response.getResult().getOutput().getText();
    }

    /**
     * 取出本次调用的元数据：用了哪个模型、消耗多少 Token。
     * 第 10 章做成本统计时就用这里的数字。
     */
    public String inspectMetadata(String userText) {
        ChatResponse response = chatModel.call(new Prompt(userText));

        String text = response.getResult().getOutput().getText();
        // Usage 里含 promptTokens / completionTokens / totalTokens
        var usage = response.getMetadata().getUsage();
        // 模型名（如 deepseek-chat / gpt-4o-mini）
        String model = response.getMetadata().getModel();

        return """
                模型：%s
                输入Token：%s  输出Token：%s  合计：%s
                回答：%s
                """.formatted(model,
                        usage.getPromptTokens(), usage.getCompletionTokens(),
                        usage.getTotalTokens(), text);
    }
}
