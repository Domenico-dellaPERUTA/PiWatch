package it.quasar_x7.backend.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity @Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class SshInfo {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String eventsJson; // memorizzare Object come stringa JSON, semplice e diretto
    private int total;
}
