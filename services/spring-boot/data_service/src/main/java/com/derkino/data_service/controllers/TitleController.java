package com.derkino.data_service.controllers;

import com.derkino.data_service.documents.Title;
import com.derkino.data_service.repositories.TitleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@RestController
public class TitleController {
    @Autowired
    MongoTemplate template;
    @Autowired
    TitleRepository repository;
    @GetMapping("/titles/{id}")
    public Title getTitle(@PathVariable String id) {
            return repository.findById(id)
                    .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    }
    @GetMapping("/titles")
    public Page<Title> getTitles(Pageable pageable,
                                 @RequestParam(required = false) String titleType,
                                 @RequestParam(required = false) String primaryTitle,
                                 @RequestParam(required = false) Boolean isAdult,
                                 @RequestParam(required = false) List<String> genres) {
        Query query = new Query();

        addQueryCriteria(query, titleType, primaryTitle, isAdult, genres);

        return getTitlesPage(query, pageable);
    }

    private PageImpl<Title> getTitlesPage(Query query, Pageable pageable) {
        query.with(pageable);

        return new PageImpl<>(template.find(query, Title.class), pageable, template.count(query, Title.class));
    }

    private static void addQueryCriteria(Query query, String titleType, String primaryTitle,
                                         Boolean isAdult, List<String> genres) {
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
    }
}
