# Script de Stress Contínuo

#!/bin/bash

# URL do gateway
URL="http://localhost:8080/api/whoami"

echo "Iniciando STRESS TEST contínuo contra $URL"
echo "Pressione CTRL + C para parar."

COUNT=0

while true; do
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
    COUNT=$((COUNT + 1))

    echo "[$COUNT] Status: $RESPONSE"

    # Pequeno delay opcional — remova para máximo estresse
    # sleep 0.01
done
