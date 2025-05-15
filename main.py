from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
import numpy as np
import joblib
import tensorflow as tf

from utils import preprocess_audio

app = FastAPI()

# Charger le modèle et l'encodeur
model = tf.keras.models.load_model("bird_classifier_yamnet_final_57_71.keras")
encoder = joblib.load("label_encoder.pkl")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Sauvegarder temporairement le fichier
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Extraire les embeddings
    embedding = preprocess_audio(file_location)

    if embedding is None:
        return JSONResponse(status_code=400, content={"error": "Problème de traitement du fichier audio."})

    # Prédiction
    prediction = model.predict(np.expand_dims(embedding, axis=0))
    predicted_index = np.argmax(prediction)
    predicted_label = encoder.inverse_transform([predicted_index])[0]

    return {"prediction": predicted_label, "confidence": float(np.max(prediction))}

