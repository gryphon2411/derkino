package com.derkino.data_service.titles;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
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
    private final TitleRepository repository;
    private final KafkaTemplate<String, String> kafkaTemplate;

    public TitleService(TitleRepository repository, KafkaTemplate<String, String> kafkaTemplate) {
        this.repository = repository;
        this.kafkaTemplate = kafkaTemplate;
    }

    public TitleDto getTitle(String id) {
        Title title = repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));

        sendToKafka(title);

        return new TitleDto(title);
    }

    public Page<TitleDto> getTitlesPage(Pageable pageable, String titleType, String primaryTitle, Boolean isAdult,
                                        List<String> genres) {
        Page<Title> titlesPage = repository.getTitlesPage(pageable, titleType, primaryTitle, isAdult, genres);
        Page<TitleDto> titlesDtoPage = titlesPage.map(TitleDto::new);

        for (Title title : titlesPage) {
            sendToKafka(title);
        }

        return titlesDtoPage;
    }

    private void sendToKafka(Title title) {
        try {
            kafkaTemplate.send("title-searches", title.id, objectMapper.writeValueAsString(title));
        } catch (JsonProcessingException exception) {
            logger.error("Couldn't send title (id: {}) to 'title-searches' topic", title.id, exception);
        }
    }

}
