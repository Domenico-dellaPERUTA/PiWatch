# agent/collector/docker_collector.py
import docker

try:
    client = docker.from_env()
except:
    client = None


def get_docker_info():
    info_docker = {
        "version": client.version()["Version"] if client else "Docker not available",
        "containers": len(client.containers.list()) if client else 0
    }
    if info_docker["containers"] > 0:
        info_docker["container_list"] = [
            {
                "id": container.id,
                "name": container.name,
                "status": container.status
            } for container in client.containers.list()
        ]
    return info_docker