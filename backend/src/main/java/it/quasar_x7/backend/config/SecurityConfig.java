// backend/src/main/java/it/quasar_x7/backend/config/SecurityConfig.java
package it.quasar_x7.backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())  // Disabilita CSRF per le API REST
            .authorizeHttpRequests(auth -> auth
                .anyRequest().permitAll()  // Permetti tutte le richieste (solo per sviluppo!)
            );
        
        return http.build();
    }
}
