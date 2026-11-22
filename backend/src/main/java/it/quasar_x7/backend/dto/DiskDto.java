package it.quasar_x7.backend.dto;

public record DiskDto(
    String total,
    String used,
    String free
) { }
