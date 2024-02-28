package com.derkino.data_service.repositories;

import com.derkino.data_service.documents.Title;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

import java.util.List;

public class CustomTitleRepositoryImpl implements CustomTitleRepository {
    @Autowired
    MongoTemplate mongoTemplate;
    
    @Override
    public Page<Title> getTitlesPage(Pageable pageable, String titleType, String primaryTitle, Boolean isAdult,
                                     List<String> genres) {
        Query query = buildTitlesQuery(titleType, primaryTitle, isAdult, genres);

        query.with(pageable);

        List<Title> content = mongoTemplate.find(query, Title.class);

        return new PageImpl<>(content, pageable, mongoTemplate.count(query, Title.class));
    }

    private Query buildTitlesQuery(String titleType, String primaryTitle, Boolean isAdult, List<String> genres) {
        Query query = new Query();

        if (titleType != null) {
            query.addCriteria(Criteria.where("titleType").is(titleType));
        }
        if (primaryTitle != null) {
            query.addCriteria(Criteria.where("primaryTitle").regex(primaryTitle, "i"));
        }
        if (isAdult != null) {
            query.addCriteria(Criteria.where("isAdult").is(isAdult));
        }
        if (genres != null && !genres.isEmpty()) {
            query.addCriteria(Criteria.where("genres").in(genres));
        }

        return query;
    }
}