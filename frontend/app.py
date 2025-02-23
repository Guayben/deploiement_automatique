import streamlit as st
import requests
from PIL import Image
import io
import os
import pandas as pd

IMAGE_FOLDER = "images"

st.markdown("<h1 style='text-align: center;'>🦴 Application de Détection de Fracture</h1>", unsafe_allow_html=True)
st.markdown("### 📤 Téléversez une image de scanner ou sélectionnez une image existante.")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("📂 Choisissez une image...", type=["jpg", "jpeg", "png"])

with col2:
    image_list = os.listdir(IMAGE_FOLDER)
    image_list = sorted([img for img in image_list if img.endswith(('.jpg', '.jpeg', '.png'))])  # Filtrer les images valides
    selected_image = st.selectbox("📸 Ou sélectionnez une image :", ["Aucune"] + image_list)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_source = "upload"
elif selected_image != "Aucune":
    image_path = os.path.join(IMAGE_FOLDER, selected_image)
    image = Image.open(image_path)
    image_source = "selection"
else:
    image = None

# Affichage de l'image sélectionnée/téléversée
if image is not None:
    st.image(image, caption="🖼️ Image sélectionnée", use_container_width=True)
    
    if st.button("🚀 Lancer la prédiction"):
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        buf.seek(0)
        
        files = {"file": ("image.jpg", buf, "image/jpeg")}
        try:
            response = requests.post("http://backend:8000/predict", files=files)
            if response.status_code == 200:
                data = response.json()
                prediction = data["prediction"]
                probability = data["probability"]
                if prediction == 0:
                    st.error(f"❌ Fracture détectée (probabilité : {1 - probability:.2f})")
                else:
                    st.success(f"✅ Aucune fracture détectée (probabilité : {probability:.2f})")
            else:
                st.error("⚠️ Erreur lors de la prédiction : " + response.text)
        except Exception as e:
            st.error("🚨 Erreur de connexion au backend : " + str(e))




# Bouton pour afficher/masquer l'architecture du modèle
if 'architecture_shown' not in st.session_state:
    st.session_state.architecture_shown = False

if st.button("🧠 Afficher/Masquer l'architecture du modèle"):
    st.session_state.architecture_shown = not st.session_state.architecture_shown

if st.session_state.architecture_shown:
    st.subheader("📜 Architecture du Modèle")
    try:
        response = requests.post("http://backend:8000/architecture")
        if response.status_code == 200:
            architecture = response.json()["architecture"]
            lines = architecture.split("\n")

            start_index = None
            end_index = None
            for i, line in enumerate(lines):
                if "Layer (type)" in line and "Output Shape" in line and "Param #" in line:
                    start_index = i + 1 
                if "Total params" in line:
                    end_index = i 
                    break

            if start_index is not None and end_index is not None:
                layer_lines = lines[start_index:end_index]
            else:
                layer_lines = []

            # Création du tableau en DataFrame pour un affichage propre
            table_data = []
            for line in layer_lines:
                parts = [part.strip() for part in line.split("│") if part.strip()]
                if len(parts) == 3: 
                    layer_type = parts[0]
                    output_shape = parts[1]
                    params = parts[2]
                    table_data.append([layer_type, output_shape, params])

            df = pd.DataFrame(table_data, columns=["Layer (type)", "Output Shape", "Parameters"])

            st.table(df)

            summary_lines = lines[end_index:] if end_index else []
            for line in summary_lines:
                if "Total params" in line:
                    st.subheader("📊 Résumé des paramètres")
                    st.markdown(f"✅ **{line.strip()}**")
                elif "Trainable params" in line:
                    st.markdown(f"🔹 **{line.strip()}**")
                elif "Non-trainable params" in line:
                    st.markdown(f"🔸 **{line.strip()}**")

        else:
            st.error("⚠️ Erreur lors de la récupération de l'architecture : " + response.text)
    except Exception as e:
        st.error(f"🚨 Erreur de connexion au backend : {str(e)}")
