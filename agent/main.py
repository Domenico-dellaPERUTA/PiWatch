# agent/main.py
import time

from collector import get_docker_info, get_ssh_connection_info, get_system_metrics


if __name__ == "__main__":
    while True:

        info = get_system_metrics()  # Ottieni metriche di sistema (CPU, RAM, Disco, OS)
        info["Docker"] = get_docker_info()  # Ottieni informazioni sui container Docker
       
        ssh_events = get_ssh_connection_info() # Ottieni informazioni sulle connessioni SSH (login riusciti, falliti, utenti invalidi)
        info["SSH"] = {
            "events": ssh_events,
            "total": len(ssh_events) if isinstance(ssh_events, list) else 0
        }
        print(f"{info}")    
        time.sleep(30)  # attesa ogni 30 secondi prima di controllare nuovamente i container
