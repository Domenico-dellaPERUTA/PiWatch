# agent/main.py
import os
import time
import requests
from collector import get_docker_info, get_ssh_connection_info, get_system_metrics

if __name__ == "__main__":
    # Legge l'URL dalle variabili d'ambiente (per Docker) o usa localhost (per test locali)
    backend_url = os.environ.get("BACKEND_URL", "http://localhost:8080")
    metrics_endpoint = f"{backend_url}/api/v1/metrics"

    while True:
        info = get_system_metrics()
        info["docker"] = get_docker_info()
        
        ssh_events = get_ssh_connection_info()
        info["ssh"] = {
            "events": ssh_events,
            "total": len(ssh_events) if isinstance(ssh_events, list) else 0
        }
        
        try:
            response = requests.post(metrics_endpoint, json=info, timeout=5)
            if response.status_code == 201:
                print(f"✅ Dati inviati con successo. Risposta: {response.text}")
            else:
                print(f"❌ Errore nell'invio. Status code: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Impossibile contattare il backend: {e}")

        time.sleep(30)