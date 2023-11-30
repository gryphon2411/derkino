package com.derkino.data_service.repositories;

import com.derkino.data_service.documents.Title;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.lang.NonNull;

import java.util.Optional;

public interface TitleRepository extends MongoRepository<Title, String> {
    @Override
    @NonNull
    Optional<Title> findById(@NonNull String id);
    Optional<Title> findByTitleConst(String titleConst);
}
