# Membres du groupe

Ce projet a été réalisé par Antoine Chanteloup, Guillaume Cazier, Lancelot Gambier, William Savre et Clément Calujek.

# Déploiement d’un Modèle d’Analyse Médicale

Ce projet est une application de classification d’images médicales permettant de détecter la présence d’une fracture osseuse sur des radiographies. Il comprend un frontend interactif (Streamlit), un backend performant (FastAPI) et une orchestration CI/CD avec Docker et GitHub Actions.

---

## Fonctionnalités

- Prédiction de fractures à partir d’une image de radiographie.
- Interface utilisateur intuitive pour téléverser et analyser les images.
- API REST avec FastAPI exposant l’inférence du modèle.
- Déploiement automatique via Docker, GitHub Actions et GitHub Container Registry (GHCR).
- Tests automatisés avec `pytest`, `Container Structure Tests`.

---

## Structure du projet

```
projet_deploiement_auto
 ┣ .github/workflows/       # Workflows GitHub Actions
 ┃ ┣ backend-ci.yml         # CI/CD du backend
 ┃ ┗ frontend-ci.yml        # CI/CD du frontend
 ┣ backend
 ┃ ┣ model                  # Fichiers du modèle (poids pré-entraînés)
 ┃ ┃ ┣ best_optimized_cnn_model.h5.keras  # Poids du modèle entraîné
 ┃ ┣ tests                  # Tests unitaires et API
 ┃ ┃ ┣ __init__.py
 ┃ ┃ ┣ container_structure_test_backend.yaml  # Tests de structure Docker
 ┃ ┃ ┗ test_api.py           # Tests de l’API backend
 ┃ ┣ app.py                 # Serveur FastAPI
 ┃ ┣ Dockerfile             # Image Docker du backend
 ┃ ┣ requirements.txt       # Dépendances du backend
 ┗ frontend
 ┃ ┣ images                 # Dossier pour stocker les images test
 ┃ ┣ tests                  # Tests du frontend
 ┃ ┃ ┣ __init__.py
 ┃ ┃ ┣ container_structure_test_frontend.yaml  # Tests de structure Docker
 ┃ ┃ ┗ test_streamlit.py     # Tests du frontend
 ┃ ┣ app.py                 # Interface utilisateur Streamlit
 ┃ ┣ Dockerfile             # Image Docker du frontend
 ┃ ┣ requirements.txt       # Dépendances du frontend
 ┣ docker-compose.yml       # Orchestration des services
 ┗ README.md                # Documentation
```

---

## Installation et Lancement

### Prérequis

- Docker et Docker Compose installés sur votre machine.

### Cloner le dépôt

```bash
git clone https://github.com/<ton-repo>/projet_deploiement_auto.git
cd projet_deploiement_auto
```

### Lancer l’application avec Docker

```bash
docker-compose up --build
```

Cela démarre :

- Le backend sur `http://localhost:8000`
- Le frontend sur `http://localhost:8501`


## Tests

### Exécuter les tests API et unitaires

```bash
cd backend
pip install -r requirements.txt
pytest tests/test_api.py
```

```bash
cd frontend
pytest tests/test_streamlit.py
```

## Déploiement Automatisé (CI/CD)

### GitHub Actions

Chaque push sur le dépôt déclenche :

1. Tests unitaires et API (`pytest`).
2. Tests de structure Docker (`Container Structure Tests`).
3. Build des images Docker (`backend` et `frontend`).
4. Push des images vers GitHub Container Registry (`GHCR`).

Les workflows sont définis dans :

```
.github/workflows/
 ├── backend-ci.yml   # CI/CD du backend
 ├── frontend-ci.yml  # CI/CD du frontend
```

