#!/bin/bash

# Attendre que la base de données soit prête
echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Initialiser la base de données
python -m app.db.init_db

# Démarrer l'application
exec uvicorn app.main:app --host 0.0.0.0 --reload