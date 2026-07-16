FROM python:3.12-slim

# Installer GDAL et ses dépendances de build
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    build-essential \
    python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*


# Éviter de travailler en root en production
RUN useradd -m appuser
WORKDIR /app

# Copier le code de l'application
COPY ./app /app/app

# Changer d’utilisateur
USER appuser

# Lancer Uvicorn (adapter module:app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--no-access-log"]

# CMD ["tail", "-f", "/dev/null" ]
