package it.quasar_x7.backend.dto;

public record MetricsDto(
    String timestamp,
    String os,
    CpuDto cpu,
    RamDto ram,
    DiskDto disk,
    DockerDto docker,
    SshDto ssh
) {}