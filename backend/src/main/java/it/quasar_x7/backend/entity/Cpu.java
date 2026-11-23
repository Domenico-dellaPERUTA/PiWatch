package it.quasar_x7.backend.entity;

import jakarta.persistence.*;
import lombok.*;


@Entity @Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Cpu {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String cores;
    private String usage;
}