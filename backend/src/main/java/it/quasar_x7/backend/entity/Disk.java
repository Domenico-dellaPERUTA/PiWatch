package it.quasar_x7.backend.entity;

import jakarta.persistence.*;
import lombok.*;


@Entity @Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Disk {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String total;
    private String used;
    private String free;
}