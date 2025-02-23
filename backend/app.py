from fastapi import FastAPI, File, UploadFile, HTTPException
import numpy as np
from PIL import Image
import io
import tensorflow as tf

app = FastAPI(title="API de détection de fracture")


model = None

@app.on_event("startup")
async def load_model_on_startup():
    global model
    try:
        model = tf.keras.models.load_model("model/best_optimized_cnn_model.h5.keras")
        print("Modèle chargé avec succès")
    except Exception as e:
        print("Erreur lors du chargement du modèle :", e)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Type de fichier non supporté")
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0) 

        prediction = model.predict(image_array)
        # Pour une classification binaire avec seuil 0.5
        prediction_label = int(prediction[0][0] >= 0.5)
        probability = float(prediction[0][0])
        return {"prediction": prediction_label, "probability": probability}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/architecture")
async def get_model_architecture():
    global model
    if model is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé")

    model_summary = []
    model.summary(print_fn=lambda x: model_summary.append(x))
    model_summary_text = "\n".join(model_summary)

    return {"architecture": model_summary_text}
