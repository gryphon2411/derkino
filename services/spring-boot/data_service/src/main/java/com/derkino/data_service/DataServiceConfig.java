package com.derkino.data_service;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class DataServiceConfig {
    @Bean
    public WebClient generativeServiceWebClient() {
        return WebClient.builder()
                .baseUrl("http://generative-service:8083/api/v1/generative")
                .build();
    }
}
