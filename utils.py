import tensorflow_hub as hub
import numpy as np
import librosa
import soundfile as sf
import tensorflow as tf

SR = 16000
AUDIO_DURATION = 20  # secondes

yamnet_model = hub.load("https://tfhub.dev/google/yamnet/1")

def preprocess_audio(file_path):
    try:
        waveform, sr = sf.read(file_path)
        if waveform.ndim > 1:
            waveform = np.mean(waveform, axis=1)
    except:
        waveform, sr = librosa.load(file_path, sr=SR, mono=True)

    waveform = waveform[:SR * AUDIO_DURATION]
    if len(waveform) < SR * AUDIO_DURATION:
        padding = SR * AUDIO_DURATION - len(waveform)
        waveform = np.pad(waveform, (0, padding))

    try:
        _, embeddings, _ = yamnet_model(waveform)
        return tf.reduce_mean(embeddings, axis=0).numpy()
    except Exception as e:
        print(f"Erreur YAMNet : {e}")
        return None
