# 1. Immagine base
FROM python:3.11-slim

# 2. Imposta la directory di lavoro
WORKDIR /app

# 3. DISABILITA IL BUFFERING DI PYTHON (fondamentale per i log in tempo reale)
ENV PYTHONUNBUFFERED=1

# 4. Installa le dipendenze di sistema per compilare psutil
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# 5. Copia SOLO requirements.txt PRIMA
COPY requirements.txt .

# 6. Aggiorna pip e installa le dipendenze Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copia il resto del codice
COPY . .

# 8. Comando di avvio (l'opzione -u è un'ulteriore sicurezza, ma ENV basta)
CMD ["python", "main.py"]
