package com.derkino.data_service.controllers;

import com.derkino.data_service.documents.Title;
import com.derkino.data_service.repositories.TitleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
public class TitleController {
    @Autowired
    TitleRepository repository;
    @GetMapping("/title/{id}")
    public Title title(@PathVariable String id) {
            return repository.findById(id)
                    .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    }
}
