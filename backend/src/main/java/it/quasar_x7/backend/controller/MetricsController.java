// backend/src/main/java/it/quasar_x7/backend/controller/MetricsController.java
package it.quasar_x7.backend.controller;

import it.quasar_x7.backend.dto.MetricsDto;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import it.quasar_x7.backend.service.*;

@RestController
@RequestMapping("/api/v1/metrics")
@CrossOrigin(origins = "*") // Utile per test iniziali, lo restringeremo con Spring Security dopo
public class MetricsController {

    private static final Logger log = LoggerFactory.getLogger(MetricsController.class);
    
    private final MetricsService service;

    public MetricsController(MetricsService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<String> receiveMetrics(@RequestBody MetricsDto metrics) {
        log.info("Ricevute metriche dal Raspberry Pi, timestamp={}", metrics.timestamp());
        var saved = service.save(metrics);
        return ResponseEntity.status(201).body("Metriche salvate, id=" + saved.getId());
    }
}