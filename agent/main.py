# agent/main.py
import docker
import time
import psutil
import platform

try:
    client = docker.from_env()
except:
    client = None

def get_raspberry_temperature():
    """Legge temperatura CPU dal sistema"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read().strip()) / 1000.0
    except FileNotFoundError:
        return None

def now():
    """Data oraria corrente in formato YYYY-MM-DD HH:MM:SS (locale)"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_ssh_connection_info():
    """Analizza auth.log per trovare eventi SSH (login riusciti, falliti, utenti invalidi)"""
    ssh_events = []
    
    try:
        with open("/var/log/auth.log", "r") as f:
            # Leggi solo le ultime 500 righe per non caricare tutto il file
            lines = f.readlines()[-500:]
            
            for line in lines:
                # Filtro: solo righe che parlano di sshd (copre sia "sshd" che "sshd-session")
                if "sshd" not in line:
                    continue
                
                # Estrai il timestamp (primi 3 campi: "Nov 20 13:44:53")
                parts = line.split()
                if len(parts) < 3:
                    continue
                timestamp = f"{parts[0]} {parts[1]} {parts[2]}"
                
                event = {"timestamp": timestamp}
                
                # Caso 1: Login riuscito
                if "Accepted" in line:
                    event["type"] = "success"
                    # Estrai il metodo: "Accepted password" o "Accepted publickey"
                    idx_accepted = parts.index("Accepted")
                    event["auth_method"] = parts[idx_accepted + 1]
                    
                    # Estrai utente (parola dopo "for")
                    if "for" in parts:
                        event["user"] = parts[parts.index("for") + 1]
                    
                    # Estrai IP (parola dopo "from")
                    if "from" in parts:
                        event["source_ip"] = parts[parts.index("from") + 1]
                    
                    # Estrai porta (parola dopo "port")
                    if "port" in parts:
                        try:
                            event["port"] = int(parts[parts.index("port") + 1])
                        except (ValueError, IndexError):
                            event["port"] = None
                    
                    ssh_events.append(event)
                
                # Caso 2: Password sbagliata
                elif "Failed password" in line:
                    event["type"] = "failed"
                    event["auth_method"] = "password"
                    
                    if "for" in parts:
                        event["user"] = parts[parts.index("for") + 1]
                    if "from" in parts:
                        event["source_ip"] = parts[parts.index("from") + 1]
                    if "port" in parts:
                        try:
                            event["port"] = int(parts[parts.index("port") + 1])
                        except (ValueError, IndexError):
                            event["port"] = None
                    
                    ssh_events.append(event)
                
                # Caso 3: Utente inesistente
                elif "Invalid user" in line:
                    event["type"] = "invalid_user"
                    event["auth_method"] = None
                    
                    if "Invalid" in parts:
                        event["user"] = parts[parts.index("Invalid") + 2]  # "Invalid" "user" "USERNAME"
                    if "from" in parts:
                        event["source_ip"] = parts[parts.index("from") + 1]
                    
                    ssh_events.append(event)
        
        return ssh_events
    
    except FileNotFoundError:
        return {"error": "auth.log non trovato"}
    except PermissionError:
        return {"error": "permessi insufficienti per leggere auth.log"}
    
if __name__ == "__main__":
    while True:
        tot_ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        free_ram = round(psutil.virtual_memory().available / (1024 ** 3), 2)
        tot_disk = round(psutil.disk_usage('/').total / (1024 ** 3), 2)
        free_disk = round(psutil.disk_usage('/').free / (1024 ** 3), 2)
        info = {
            "timestamp": now(),
            "OS": f"{platform.system()} {platform.release()}",
            "CPU": { 
                "cores": f"{psutil.cpu_count(logical=True)} cores",
                "usage": f"{psutil.cpu_percent(interval=1)}%"
            },
            "RAM": { 
                "total": f"{tot_ram} GB",
                "used": f"{round((tot_ram - free_ram) / tot_ram * 100, 2)}%",
                "available": f"{free_ram} GB"
            },
            "Disk": {
                "total": f"{tot_disk} GB",
                "used": f"{round((tot_disk - free_disk) / tot_disk * 100, 2)}%",
                "free": f"{free_disk} GB"
            },
            "Docker": {
                "version": client.version()["Version"] if client else "Docker not available",
                "containers": len(client.containers.list()) if client else 0
            }
        }
        
        if info["Docker"]["containers"] > 0:
            info["Docker"]["container_list"] = [
                {
                    "id": container.id,
                    "name": container.name,
                    "status": container.status
                } for container in client.containers.list()
            ]

        temperature = get_raspberry_temperature()
        if temperature is not None:
            info["temperature"] = f"{temperature}°C"

        ssh_events = get_ssh_connection_info()
        info["SSH"] = {
            "events": ssh_events,
            "total": len(ssh_events) if isinstance(ssh_events, list) else 0
        }
        print(f"{info}")    
        time.sleep(30)  # attesa ogni 30 secondi prima di controllare nuovamente i container
