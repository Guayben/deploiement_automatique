# frontend/app.py
import streamlit as st
import requests
from PIL import Image
import io

st.title("Application de détection de fracture")
st.write("Téléversez une image de scanner pour détecter une fracture.")

uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Image téléversée", use_container_width=True)
    
    if st.button("Lancer la prédiction"):
        # Conversion de l'image en bytes
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        buf.seek(0)
        
        files = {"file": ("image.jpg", buf, "image/jpeg")}
        try:
            # On suppose que le backend est accessible via le nom de service "backend"
            response = requests.post("http://backend:8000/predict", files=files)
            if response.status_code == 200:
                data = response.json()
                prediction = data["prediction"]
                probability = data["probability"]
                if prediction <= 0.5:
                    st.error(f"Fracture détectée (probabilité : {1-probability:.2f})")
                else:
                    st.success(f"Aucune fracture détectée (probabilité : {probability:.2f})")
            else:
                st.error("Erreur lors de la prédiction : " + response.text)
        except Exception as e:
            st.error("Erreur de connexion au backend : " + str(e))
