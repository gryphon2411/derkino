package com.derkino.auth_service;

import com.derkino.auth_service.customuser.CustomUser;
import com.derkino.auth_service.customuser.CustomUserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.security.crypto.factory.PasswordEncoderFactories;

@SpringBootApplication
public class AuthServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(AuthServiceApplication.class, args);
	}
	@Bean
	public CommandLineRunner demo(CustomUserRepository repository) {
		return (args) -> {
			String encodedPassword = PasswordEncoderFactories.createDelegatingPasswordEncoder().encode("password");

			repository.save(new CustomUser("user", "user@example.com", encodedPassword));
		};
	}
}
