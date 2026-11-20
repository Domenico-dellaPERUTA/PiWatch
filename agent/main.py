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



if __name__ == "__main__":
    while True:
        tot_ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        free_ram = round(psutil.virtual_memory().available / (1024 ** 3), 2)
        tot_disk = round(psutil.disk_usage('/').total / (1024 ** 3), 2)
        free_disk = round(psutil.disk_usage('/').free / (1024 ** 3), 2)
        info = {
            "timestamp": now(),
            "OS": f"{platform.system()} {platform.release()}",
            "CPU": f"{psutil.cpu_count(logical=True)} cores",
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
        
        print(f"{info}")    
        time.sleep(30)  # attesa ogni 30 secondi prima di controllare nuovamente i container
