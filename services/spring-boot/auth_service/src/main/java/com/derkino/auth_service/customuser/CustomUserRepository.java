package com.derkino.auth_service.customuser;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface CustomUserRepository extends MongoRepository<CustomUser, String> {
	CustomUser findCustomUserByUsername(String username);
}
