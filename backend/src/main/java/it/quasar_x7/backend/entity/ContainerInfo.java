package it.quasar_x7.backend.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity @Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class ContainerInfo {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String containerId; // evitare "id" per non confondere con la chiave primaria
    private String name;
    private String status;
}