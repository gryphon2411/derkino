package com.derkino.data_service.services;

import com.derkino.data_service.documents.Title;
import com.derkino.data_service.repositories.TitleRepository;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
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
    TitleRepository repository;
    @Autowired
    KafkaTemplate<String, String> kafkaTemplate;

    public Title getTitle(String id) {
        Title title = repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));

        sendToKafka(title);

        return title;
    }

    public Page<Title> getTitlesPage(Pageable pageable, String titleType, String primaryTitle, Boolean isAdult,
                                     List<String> genres) {
        Page<Title> page = repository.getTitlesPage(pageable, titleType, primaryTitle, isAdult, genres);

        for (Title title : page) {
            sendToKafka(title);
        }

        return page;
    }

    private void sendToKafka(Title title) {
        try {
            kafkaTemplate.send("title-searches", title.id, objectMapper.writeValueAsString(title));
        } catch (JsonProcessingException exception) {
            logger.error("Couldn't send title (id: {}) to 'title-searches' topic", title.id, exception);
        }
    }

}
