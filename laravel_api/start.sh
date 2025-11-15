#!/bin/sh
set -e
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
echo "Aguardando o PostgreSQL ($DB_HOST:$DB_PORT) iniciar para API..."
until nc -z $DB_HOST $DB_PORT >/dev/null 2>&1; do
  echo "PostgreSQL indisponível - aguardando..."
  sleep 1
done
echo "PostgreSQL está pronto."
echo "Executando composer install..."
composer install --no-interaction --prefer-dist --optimize-autoloader
exec "$@"
