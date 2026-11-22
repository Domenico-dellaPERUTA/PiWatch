package it.quasar_x7.backend.dto;

import java.util.List;

public record DockerDto(
    String version,
    int containers,
    List<ContainerDto> containerList // Jackson lo mapperà a null se non presente nel JSON
) {}