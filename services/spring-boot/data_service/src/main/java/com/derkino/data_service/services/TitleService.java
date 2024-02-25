package com.derkino.data_service.services;

import com.derkino.data_service.documents.Title;
import com.derkino.data_service.repositories.TitleRepository;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.http.HttpStatus;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@Service
public class TitleService {
    private static final Logger logger = LoggerFactory.getLogger(TitleService.class);
    private final ObjectMapper objectMapper = new ObjectMapper();
    @Autowired
    MongoTemplate mongoTemplate;
    @Autowired
    TitleRepository repository;
    @Autowired
    KafkaTemplate<String, String> kafkaTemplate;

    public Title getTitle(String id) {
        Title title = repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));

        sendToKafka(title);

        return title;
    }

    public Page<Title> getTitles(Pageable pageable, String titleType, String primaryTitle, Boolean isAdult,
                                 List<String> genres) {
        Query query = new Query();

        addQueryCriteria(query, titleType, primaryTitle, isAdult, genres);

        return getTitlesPage(query, pageable);
    }

    private PageImpl<Title> getTitlesPage(Query query, Pageable pageable) {
        query.with(pageable);

        List<Title> content = mongoTemplate.find(query, Title.class);

        for (Title title : content) {
            sendToKafka(title);
        }

        return new PageImpl<>(content, pageable, mongoTemplate.count(query, Title.class));
    }

    private void sendToKafka(Title title) {
        try {
            kafkaTemplate.send("title-searches", title.id, objectMapper.writeValueAsString(title));
        } catch (JsonProcessingException exception) {
            logger.error("Couldn't send title (id: {}) to 'title-searches' topic", title.id, exception);
        }
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
