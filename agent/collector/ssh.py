# agent/collector/ssh.py
#
# Informazioni connessioni SSH (Parsing auth.log)

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
 