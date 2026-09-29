package com.example.springai;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 工程入口。
 *
 * @SpringBootApplication 是三个注解的合并简写：
 *   1. @SpringBootConfiguration —— 声明这是一个配置类（本质是 @Configuration）
 *   2. @EnableAutoConfiguration —— 按类路径自动装配，比如检测到 WebMVC 就配好 MVC，
 *      检测到 spring-ai-starter-model-openai 就配好 ChatModel / ChatClient.Builder
 *   3. @ComponentScan           —— 自动扫描本包（com.example.springai）及子包下的所有 Bean
 *
 * 注意：主类必须放在所有业务类的"上层"包，否则 @ComponentScan 扫不到。
 */
@SpringBootApplication
public class SpringaiLabApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringaiLabApplication.class, args);
    }
}
