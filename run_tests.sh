#!/bin/bash

# Lancer les conteneurs
docker-compose up -d

# Attendre que la base de données de test soit prête
echo "Waiting for test database to be ready..."
docker-compose run api bash -c 'while ! nc -z test_db 5432; do sleep 0.1; done'

# Exécuter les tests
docker-compose run api pytest app/tests -v

# Arrêter les conteneurs
docker-compose down