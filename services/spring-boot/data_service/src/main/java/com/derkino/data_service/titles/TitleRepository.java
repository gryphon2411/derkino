package com.derkino.data_service.titles;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface TitleRepository extends MongoRepository<Title, String>, CustomTitleRepository { }
