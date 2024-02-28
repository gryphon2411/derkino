package com.derkino.data_service.repositories;

import com.derkino.data_service.documents.Title;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface TitleRepository extends MongoRepository<Title, String>, CustomTitleRepository { }
