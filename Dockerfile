# Utiliser une image Python slim
FROM python:3.13-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt depuis la racine
COPY ./requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le fichier de migration depuis le dossier app
COPY ./app/migration.py /app/

# Copier le dossier data (dossier contenant des fichiers CSV, etc.)
COPY ./data /app/data

# Exposer le point d'entrée
CMD ["python", "migration.py"]
