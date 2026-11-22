# Pi Watch 

### Sistema di monitoraggio Raspberry

PiWatch è un sistema di monitoraggio che raccoglie metriche di sistema, stato dei container 
Docker e accessi SSH, le aggrega in un backend e le visualizza in una dashboard web.



```
┌─────────────────────────────────────────────────────────┐
│                   RASPBERRY PI                          │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────┐   │
│  │   Agent      │──▶│  Spring Boot │──▶│ PostgreSQL │   │
│  │  (Python)    │   │   Backend    │   │            │   │
│  │  raccoglie   │   │   API + JWT  │   │   dati     │   │
│  │   i dati     │   │              │   │            │   │
│  └──────────────┘   └──────┬───────┘   └────────────┘   │
│                            │                            │
│                     ┌──────▼───────┐                    │
│                     │    React     │                    │
│                     │  Dashboard   │                    │
│                     │  (browser)   │                    │
│                     └──────────────┘                    │
│                                                         │
│  [Access Point] [Container Docker] [SSH] [Sistema]      │
└─────────────────────────────────────────────────────────┘
```

## Struttura del progetto


```
piwatch/
├── agent/            # Python agent
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── collector/
│       ├── system.py      # temperatura, RAM, CPU
│       ├── docker.py      # stato container
│       └── ssh.py         # log accessi SSH
│
├── backend/          # Spring Boot
│   ├── Dockerfile
│   ├── pom.xml
│   └── src/
│       src/
│       └── main/
│           ├── java/
│           │   └── it/
│           │       └── quasar_x7/
│           │           └── backend/
│           │               ├── BackendApplication.java      
│           │               ├── dto/                         
│           │               │   ├── CpuDto.java
│           │               │   ├── RamDto.java
│           │               │   ├── DiskDto.java
│           │               │   ├── ContainerDto.java
│           │               │   ├── DockerDto.java
│           │               │   ├── SshDto.java
│           │               │   └── MetricsDto.java
│           │               └── controller/                  
│           │                   └── MetricsController.java
│           └── resources/
│               └── application.properties                   
│
├── frontend/         # React
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── components/
│       ├── pages/
│       └── api/
│
├── docker-compose.yml          # Orchestrazione
├── docker-compose.prod.yml     # Override per produzione
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions
└── README.md
```


## 🛠️ Tech Stack

| Componente | Tecnologia |
|------------|-----------|
| Agent | Python 3 + psutil + docker-py |
| Backend | Spring Boot 3 + Java 17 + Spring Security (JWT) |
| Frontend | React + TypeScript + Vite + TailwindCSS |
| Database | PostgreSQL 15 |
| Deploy | Docker Compose + GitHub Actions (CI/CD) |

## 📊 Cosa monitora

- [ ] Stato di tutti i container Docker (anche quelli preesistenti)
- [ ] Temperatura CPU (sospetto n.1 per gli spegnimenti)
- [ ] Utilizzo RAM e CPU
- [ ] Accessi SSH (successi e tentativi falliti)
- [ ] Uptime e reboot
- [ ] Log kernel (OOM killer, panic)

