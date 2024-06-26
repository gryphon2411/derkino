package com.derkino.auth_service.secured;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class SecuredController {
    @GetMapping("/secured")
    public ResponseEntity<Map<String, String>> secured() {
        return ResponseEntity.ok(Map.of("message", "Secured content"));
    }
}
