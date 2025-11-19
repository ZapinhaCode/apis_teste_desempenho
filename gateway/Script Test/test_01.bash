#!/bin/bash

# Defina a URL do gateway
GATEWAY_URL="http://localhost:5004/api/whoami"
# Defina a quantidade de requisições simultâneas
REQUESTS=2

echo "Enviando $REQUESTS requisições simultâneas para o gateway..."
echo "----------------------------------------"

seq 1 $REQUESTS | xargs -n1 -P$REQUESTS -I{} curl -s $GATEWAY_URL

echo ""
echo "----------------------------------------"
echo "Teste finalizado."
