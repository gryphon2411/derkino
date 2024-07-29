package com.derkino.data_service.titles;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.server.ResponseStatusException;

import java.time.Duration;
import java.util.List;
import java.util.Map;

@Service
public class TitleService {
    private static final Logger logger = LoggerFactory.getLogger(TitleService.class);
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final TitleRepository repository;
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final WebClient generativeServiceWebClient;

    public TitleService(TitleRepository repository, KafkaTemplate<String, String> kafkaTemplate,
                        @Qualifier("generativeServiceWebClient") WebClient generativeServiceWebClient) {
        this.repository = repository;
        this.kafkaTemplate = kafkaTemplate;
        this.generativeServiceWebClient = generativeServiceWebClient;
    }

    public TitleDto getTitle(String id) {
        Title title = repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));

        sendToKafka(title);

        TitleDto titleDto = new TitleDto(title);
        titleDto.facts = getTitleFacts(title);

        return titleDto;
    }

    private String getTitleFacts(Title title) {
        String facts = null;

        try {
            facts = this.generativeServiceWebClient
                    .post()
                    .uri("/title/facts")
                    .bodyValue(Map.of("title_name", title.primaryTitle, "title_year", title.endYear))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .blockOptional(Duration.ofSeconds(10))
                    .map(response -> (String) response.get("facts"))
                    .orElse(null);
        } catch (Exception exception) {
            logger.error("Couldn't generate facts for title: {}", title, exception);
        }
        return facts;
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
