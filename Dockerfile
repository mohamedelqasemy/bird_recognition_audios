# Étape 1 : Image de base avec Python
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers nécessaires
COPY . /app

# Étape 4 : Installer les dépendances système
RUN apt-get update && apt-get install -y \
    ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Étape 5 : Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Étape 6 : Exposer le port
EXPOSE 8003

# Étape 7 : Commande de lancement de l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
