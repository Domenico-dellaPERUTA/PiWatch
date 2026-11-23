package it.quasar_x7.backend.entity;

import jakarta.persistence.*;
import lombok.*;


@Entity @Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class DockerInfo {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String version;
    private int containers;

    @OneToMany(cascade = CascadeType.ALL)
    @JoinColumn(name = "docker_id")
    private java.util.List<ContainerInfo> containerList;
}