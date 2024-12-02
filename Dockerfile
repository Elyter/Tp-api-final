FROM python:3.11

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y netcat-traditional

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer un script de démarrage directement dans le Dockerfile
RUN echo '#!/bin/bash\n\
echo "Waiting for database to be ready..."\n\
while ! nc -z db 5432; do\n\
  sleep 0.1\n\
done\n\
echo "Database is ready!"\n\
\n\
python -m app.db.init_db\n\
\n\
exec uvicorn app.main:app --host 0.0.0.0 --reload' > /app/start.sh

# Donner les permissions d'exécution
RUN chmod +x /app/start.sh

# Utiliser le nouveau script
CMD ["/app/start.sh"]
