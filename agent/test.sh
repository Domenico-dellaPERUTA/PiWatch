#!/bin/bash
set -e

echo "🔄 Ricostruzione dell'immagine..."

# Verifica se siamo già nella cartella agent o se dobbiamo entrarci
if [ "$(basename "$PWD")" != "agent" ]; then
    echo "📂 Entro nella cartella agent..."
    cd agent
else
    echo "✅ Sono già nella cartella agent"
fi

docker build -t piwatch-agent .

echo "🚀 Avvio del container..."
# Rimuovi eventuali container vecchi con lo stesso nome
docker rm -f piwatch-agent 2>/dev/null || true

# Avvia il container in background
docker run -d --name piwatch-agent --rm -v /var/run/docker.sock:/var/run/docker.sock:ro piwatch-agent

echo "✅ Container avviato."
echo ""
echo "📋 Mostro i log per 30 secondi, poi il container verrà arrestato automaticamente..."
echo "   (Premi Ctrl+C ORA se vuoi interrompere subito e tornare al prompt)"
echo "---------------------------------------------------"

# 1. Avvia i log in background e salva il suo Process ID (PID)
docker logs -f piwatch-agent &
LOGS_PID=$!

# 2. Attendi 30 secondi
sleep 30

# 3. Termina il processo dei log (silenziosamente se già terminato)
kill $LOGS_PID 2>/dev/null || true

echo "---------------------------------------------------"
echo "⏹️ Arresto del container..."
docker stop piwatch-agent
echo "✅ Fatto!"