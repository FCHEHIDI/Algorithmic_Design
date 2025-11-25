# 🐳 Dockerfile - Lab Planner V3 Optimisé

# ============================================
# STAGE 1 : Builder - Construction de l'image
# ============================================
FROM python:3.11-slim as builder

# Métadonnées de l'image
LABEL maintainer="algorithmic-design@example.com"
LABEL version="3.0"
LABEL description="Planificateur de laboratoire optimisé avec architecture OOP et concurrence"

# Définir le répertoire de travail
WORKDIR /app

# Variables d'environnement pour Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copier uniquement les fichiers de dépendances d'abord (pour le cache Docker)
COPY v3_optimized/requirements.txt .

# Installer les dépendances (s'il y en a dans le futur)
# Pour l'instant, V3 n'utilise que la stdlib Python
RUN pip install --no-cache-dir -r requirements.txt || true

# ============================================
# STAGE 2 : Runtime - Image finale légère
# ============================================
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app \
    LOG_LEVEL=INFO

# Créer un utilisateur non-root pour la sécurité
RUN groupadd -r labplanner && useradd -r -g labplanner labplanner

# Définir le répertoire de travail
WORKDIR /app

# Copier l'application depuis le builder
COPY --chown=labplanner:labplanner v3_optimized/ .

# Créer les dossiers nécessaires
RUN mkdir -p logs output && \
    chown -R labplanner:labplanner /app

# Passer à l'utilisateur non-root
USER labplanner

# Exposer un port (pour une future API REST)
EXPOSE 8000

# Healthcheck (vérifie que le module s'importe correctement)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "from lab_planner import LabPlanner; print('OK')" || exit 1

# Point d'entrée par défaut : exécuter le programme principal
ENTRYPOINT ["python", "main.py"]

# Arguments par défaut (peuvent être surchargés)
CMD []
