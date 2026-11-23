# agent/main.py
import time
import requests

from collector import get_docker_info, get_ssh_connection_info, get_system_metrics


if __name__ == "__main__":
    while True:

        info = get_system_metrics()  # Ottieni metriche di sistema (CPU, RAM, Disco, OS)
        info["docker"] = get_docker_info()  # Ottieni informazioni sui container Docker
       
        ssh_events = get_ssh_connection_info() # Ottieni informazioni sulle connessioni SSH (login riusciti, falliti, utenti invalidi)
        info["ssh"] = {
            "events": ssh_events,
            "total": len(ssh_events) if isinstance(ssh_events, list) else 0
        }
        print(f"{info}")

        try:
            response = requests.post("http://localhost:8080/api/v1/metrics", json=info)
            if response.status_code == 200:
                print("Dati inviati con successo al server.")
            else:
                print(f"Errore nell'invio dei dati al server. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Errore nella richiesta al server: {e}")

        time.sleep(30)  # attesa ogni 30 secondi prima di controllare nuovamente i container
