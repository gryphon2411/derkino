package com.derkino.data_service;

import org.springframework.context.annotation.Bean;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

public class DataServiceSecurityConfig {
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .cors(Customizer.withDefaults())
                .csrf(csrf ->
                        csrf
                                .ignoringRequestMatchers("/titles", "/secured"))

                .authorizeHttpRequests(authorize ->
                        authorize
                                .anyRequest().authenticated())

                /* The default implementation of SecurityContextRepository is
                    DelegatingSecurityContextRepository which delegates to:
                        1. HttpSessionSecurityContextRepository
                        2. RequestAttributeSecurityContextRepository
                 */

                // By default, authentication will be persisted and restored on future requests.

                // By default, anonymous authentication is provided automatically

                // By default, Spring Security stands up a /logout endpoint.

                .rememberMe(Customizer.withDefaults());

        return http.build();
    }
}
