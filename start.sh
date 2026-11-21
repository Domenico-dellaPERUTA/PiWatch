#!/bin/bash
set -e

echo "🚀 Avvio dei container..."
docker-compose up -d

docker-compose logs -f agent