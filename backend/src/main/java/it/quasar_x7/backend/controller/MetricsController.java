package it.quasar_x7.backend.controller;

import it.quasar_x7.backend.dto.MetricsDto;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/metrics")
@CrossOrigin(origins = "*") // Utile per test iniziali, lo restringeremo con Spring Security dopo
public class MetricsController {

    private static final Logger log = LoggerFactory.getLogger(MetricsController.class);

    @PostMapping
    public ResponseEntity<String> receiveMetrics(@RequestBody MetricsDto metrics) {
        log.info("✅ Metriche ricevute dal Raspberry Pi!");
        log.info("   Timestamp: {}", metrics.timestamp());
        log.info("   OS: {}", metrics.os());
        log.info("   CPU Usage: {}", metrics.cpu().usage());
        log.info("   RAM Available: {}", metrics.ram().available());
        log.info("   Docker Containers: {}", metrics.docker().containers());
        
        // TODO: Qui in futuro chiameremo il Service per salvare su PostgreSQL
        
        return ResponseEntity.ok("Metriche ricevute e processate con successo");
        // In produzione, restituiremmo un 201 Created o un DTO di risposta
    }
}