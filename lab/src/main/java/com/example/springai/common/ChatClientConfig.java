package com.example.springai.common;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.SimpleLoggerAdvisor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 全局 ChatClient 配置。
 *
 * 为什么不直接在 Service 里 new？
 * —— 因为默认系统提示、默认 Advisor 应该全应用统一，
 *    散落在各个 Service 里迟早改不齐。
 *
 * 注意：容器里已经有一个 ChatClient.Builder（Spring AI 自动装配），
 * 我们注入它再 build，比自己 new Builder 更省事。
 */
@Configuration
public class ChatClientConfig {

    @Bean
    public ChatClient chatClient(ChatClient.Builder builder) {
        return builder
                // 全局默认角色设定：所有请求都会自动带上（可在单次调用时覆盖）
                .defaultSystem("""
                        你是"智汇企业助手"，服务于公司内部员工。
                        规则：
                        1. 用简体中文回答，语气专业但不啰嗦。
                        2. 不确定的信息必须说明"我需要更多信息"，禁止编造。
                        3. 涉及金额、日期、人名时，严格使用原文给出的数据。
                        """)
                // 默认 Advisor：打印每次请求/响应，调试期必开（第 3 章会写自定义的）
                .defaultAdvisors(new SimpleLoggerAdvisor())
                // 不在这里写 defaultOptions，留给各场景按需覆盖
                .build();
    }
}
