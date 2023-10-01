#!/bin/bash

# FILE TO BE RAN INSIDE DOCKER CONTAINER

# the container names are defined in docker-compose.yml
until nc -z spa_db 5432; do
    echo "$(date) - waiting for postgres container to get up ..."
    sleep 1
done

export PYTHONPATH=$PYTHONPATH:$(pwd)/app

createdb -U $POSTGRES_USER $POSTGRES_DB

echo "Migrating schema..." && echo
alembic upgrade head

echo "Downloading data"
bash /app/scripts/prepare_data.sh

echo "Initializing DB [may take up to 20 minutes]..."
python /app/scripts/populate_db.py

echo "Running the app..." && echo
uvicorn app.main:app --host 0.0.0.0 --port 9999