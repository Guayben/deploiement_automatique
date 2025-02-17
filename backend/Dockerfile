# backend/Dockerfile
FROM python:3.11.11-slim

WORKDIR /app

# Mise à jour et installation des dépendances système si nécessaire
RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
