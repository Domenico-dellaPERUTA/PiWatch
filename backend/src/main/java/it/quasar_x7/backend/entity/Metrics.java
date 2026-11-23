package it.quasar_x7.backend.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "metrics")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Metrics {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String timestamp;
    private String os;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "cpu_id")
    private Cpu cpu;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "ram_id")
    private Ram ram;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "disk_id")
    private Disk disk;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "docker_id")
    private DockerInfo docker;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "ssh_id")
    private SshInfo ssh;
}