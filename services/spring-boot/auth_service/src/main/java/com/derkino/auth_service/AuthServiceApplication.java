package com.derkino.auth_service;

import com.derkino.auth_service.customuser.CustomUser;
import com.derkino.auth_service.customuser.CustomUserRepository;
// import com.derkino.auth_service.customuser.MapCustomUserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.HashMap;
import java.util.Map;

@SpringBootApplication
public class AuthServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(AuthServiceApplication.class, args);
	}
	@Bean
	public CommandLineRunner demo(CustomUserRepository repository) {
		return (args) -> {
			String encodedPassword = "{bcrypt}$2a$10$h/AJueu7Xt9yh3qYuAXtk.WZJ544Uc2kdOKlHu2qQzCh/A3rq46qm";
			repository.save(new CustomUser("user@example.com",encodedPassword));
		};
	}

//	@Bean
//	MapCustomUserRepository userRepository() {
//		// the hashed password was calculated using the following code
//		// the hash should be done up front, so malicious users cannot discover the
//		// password
//		// PasswordEncoder encoder =
//		// PasswordEncoderFactories.createDelegatingPasswordEncoder();
//		// String encodedPassword = encoder.encode("password");
//
//		// the raw password is "password"
//		String encodedPassword = "{bcrypt}$2a$10$h/AJueu7Xt9yh3qYuAXtk.WZJ544Uc2kdOKlHu2qQzCh/A3rq46qm";
//
//		CustomUser customUser = new CustomUser("user@example.com", encodedPassword);
//		Map<String, CustomUser> emailToCustomUser = new HashMap<>();
//		emailToCustomUser.put(customUser.getEmail(), customUser);
//		return new MapCustomUserRepository(emailToCustomUser);
//	}
}
