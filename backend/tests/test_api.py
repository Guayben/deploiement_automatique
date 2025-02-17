# backend/tests/test_api.py
import io
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_invalid_file():
    response = client.post(
        "/predict",
        files={"file": ("test.txt", b"notanimage", "text/plain")}
    )
    assert response.status_code == 400

def test_predict_valid_file():
    # Création d'une image blanche de 224x224
    from PIL import Image
    import numpy as np
    image = Image.fromarray(np.uint8(255 * np.ones((224, 224, 3))), "RGB")
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)
    
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", buf, "image/jpeg")}
    )
    # Pour ce test, on s'attend à recevoir un résultat même si le modèle n'est pas entraîné
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
