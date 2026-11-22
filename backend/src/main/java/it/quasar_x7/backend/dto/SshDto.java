package it.quasar_x7.backend.dto;



public record SshDto(
    Object events, // Può essere una Lista (se ci sono eventi) o una Mappa (se c'è un errore)
    int total
) {}