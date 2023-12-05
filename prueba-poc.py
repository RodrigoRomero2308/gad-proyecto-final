import os
import librosa
import librosa.display
import numpy as np
import pandas as pd

# Función para extraer características de un archivo de audio
def extract_audio_features(audio_file):
    # Cargar el archivo de audio
    y, sr = librosa.load(audio_file)

    # Calcular el tono (pitch) usando el algoritmo de YIN
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_mean = np.mean(pitches[pitches > 0]) if np.sum(pitches > 0) > 0 else 0

    # Calcular los coeficientes cepstrales de frecuencia de Mel (MFCCs)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Combinar las características en un vector
    features = [pitch_mean] + list(np.mean(mfccs, axis=1))

    return features

# Carpeta que contiene los archivos de audio
audio_folder = "D:\\Downloads\\distintaEspecie"

# Lista para almacenar las características de todos los archivos
all_audio_features = []

# Recorrer todos los archivos de audio en la carpeta
for root, dirs, files in os.walk(audio_folder):
    for file in files:
        if file.endswith(".mp3"):
            audio_file = os.path.join(root, file)
            print(f"Procesando: {audio_file}")

            # Extraer características del archivo de audio
            features = extract_audio_features(audio_file)

            # Almacenar las características en la lista
            all_audio_features.append(features)

# Convertir las características a un DataFrame
feature_names = ['Pitch', 'MFCC1', 'MFCC2', 'MFCC3', 'MFCC4', 'MFCC5', 'MFCC6', 'MFCC7', 'MFCC8', 'MFCC9', 'MFCC10', 'MFCC11', 'MFCC12', 'MFCC13']
features_df = pd.DataFrame(all_audio_features, columns=feature_names)

# Guardar el DataFrame en un archivo CSV
features_df.to_csv("audio_features_distintos.csv", index=False)
