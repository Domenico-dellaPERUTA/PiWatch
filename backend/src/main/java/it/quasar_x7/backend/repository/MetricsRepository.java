package it.quasar_x7.backend.repository;

import it.quasar_x7.backend.entity.Metrics;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MetricsRepository extends JpaRepository<Metrics, Long> {
}