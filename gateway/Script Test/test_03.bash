# Script de Carga Gradual

#!/bin/bash

URL="http://localhost:8080/api/whoami"

echo "🚀 Iniciando LOAD TEST (carga gradual)"
echo "➡ API alvo: $URL"
echo ""

# Número inicial de usuários
START=1

# Número máximo de usuários simultâneos
MAX=200

# Incremento por etapa
STEP=10

# Tempo de teste por etapa (em segundos)
DURATION=5

for USERS in $(seq $START $STEP $MAX); do
    echo "---------------------------------------"
    echo "🔸 Rodando com $USERS usuários..."
    echo "---------------------------------------"

    # Inicia $USERS requisições simultâneas durante $DURATION segundos
    for i in $(seq 1 $USERS); do
        (
            END=$((SECONDS + DURATION))
            while [ $SECONDS -lt $END ]; do
                curl -s -o /dev/null "$URL"
            done
        ) &
    done

    # Espera todos os processos dessa fase
    wait
done

echo ""
echo "✅ Teste de carga gradual finalizado!"
