package it.quasar_x7.backend.service;

import it.quasar_x7.backend.dto.*;
import it.quasar_x7.backend.entity.*;
import it.quasar_x7.backend.repository.MetricsRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class MetricsService {

    private final MetricsRepository repository;

    @Transactional
    public Metrics save(MetricsDto dto) {
        Metrics m = new Metrics();
        m.setTimestamp(dto.timestamp());
        m.setOs(dto.os());

        if (dto.cpu() != null) {
            m.setCpu(Cpu.builder()
                    .cores(dto.cpu().cores())
                    .usage(dto.cpu().usage())
                    .build());
        }
        if (dto.ram() != null) {
            m.setRam(Ram.builder()
                    .total(dto.ram().total())
                    .used(dto.ram().used())
                    .available(dto.ram().available())
                    .build());
        }
        if (dto.disk() != null) {
            m.setDisk(Disk.builder()
                    .total(dto.disk().total())
                    .used(dto.disk().used())
                    .free(dto.disk().free())
                    .build());
        }
        if (dto.docker() != null) {
            DockerInfo di = new DockerInfo();
            di.setVersion(dto.docker().version());
            di.setContainers(dto.docker().containers());
            if (dto.docker().containerList() != null) {
                di.setContainerList(dto.docker().containerList().stream()
                        .map(c -> ContainerInfo.builder()
                                .containerId(c.id())
                                .name(c.name())
                                .status(c.status())
                                .build())
                        .collect(Collectors.toList()));
            }
            m.setDocker(di);
        }
        if (dto.ssh() != null) {
            SshInfo si = new SshInfo();
            si.setTotal(dto.ssh().total());
            si.setEventsJson(dto.ssh().events() != null ? dto.ssh().events().toString() : null);
            m.setSsh(si);
        }

        return repository.save(m);
    }
}