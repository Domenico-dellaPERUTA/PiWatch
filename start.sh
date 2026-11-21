#!/bin/bash
set -e

echo "🚀 Avvio dei container e costruzione delle immagini..."
docker-compose up -d  --build

docker-compose logs -f agent