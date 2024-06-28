package com.derkino.auth_service.login;

import com.derkino.auth_service.customuser.CustomUser;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.context.SecurityContextRepository;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LoginController {
    private final AuthenticationManager authenticationManager;
    private final SecurityContextRepository securityContextRepository;

    public LoginController(AuthenticationManager authenticationManager,
                           SecurityContextRepository securityContextRepository) {
        this.authenticationManager = authenticationManager;
        this.securityContextRepository = securityContextRepository;
    }

    @PostMapping("/login")
    public ResponseEntity<CustomUser> login(HttpServletRequest request, HttpServletResponse response,
                                            @RequestBody LoginRequest loginRequest) {
        Authentication authentication = this.authenticate(loginRequest);
        this.setAuthentication(authentication, request, response);

        CustomUser principal = (CustomUser) authentication.getPrincipal();

        principal.password = null;

        return ResponseEntity.ok(principal);
    }

    private void setAuthentication(Authentication authentication, HttpServletRequest request,
                                   HttpServletResponse response) {
        SecurityContext context = SecurityContextHolder.getContext();
        context.setAuthentication(authentication);
        this.securityContextRepository.saveContext(context, request, response);
    }

    private Authentication authenticate(LoginRequest loginRequest) {
        UsernamePasswordAuthenticationToken token =
                UsernamePasswordAuthenticationToken.unauthenticated(loginRequest.username(), loginRequest.password());

        return this.authenticationManager.authenticate(token);
    }

    public record LoginRequest(String username, String password) { }
}
