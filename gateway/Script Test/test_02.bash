#!/bin/bash

GATEWAY_URL="http://localhost:8080/api/whoami"

echo "Iniciando teste de stress contínuo no gateway..."
echo "Pressione CTRL + C para parar."
echo "----------------------------------------"

while true
do
  curl -s $GATEWAY_URL > /dev/null
done