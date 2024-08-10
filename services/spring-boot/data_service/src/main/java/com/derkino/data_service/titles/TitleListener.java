package com.derkino.data_service.titles;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;

@Component
public class TitleListener {
    private final TitleService service;

    public TitleListener(TitleService service) {
        this.service = service;
    }

    @RabbitListener(queues = "derkino.data_service.title.rpc.requests", errorHandler = "rabbitListenerErrorHandler")
    public TitleDto getTitle(TitleRequest request) {
        return service.getTitle(request.title_id())
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND, HttpStatus.NOT_FOUND.getReasonPhrase())
                );
    }
}

record TitleRequest(String title_id) { }
