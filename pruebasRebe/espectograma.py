import os
import librosa
import librosa.display
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Función para extraer características de un archivo de audio
def extract_audio_features(audio_file):
    # Cargar el archivo de audio
    y, sr = librosa.load(audio_file)

    # Calcular el espectrograma de Mel
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

    # Guardar el espectrograma en un archivo
    np.save(audio_file.replace(".mp3", "_mel_spectrogram.npy"), mel_spectrogram)

# Carpeta que contiene los archivos de audio
audio_folder = "parecidos"
#audio_folder = "distintos"

# Lista para almacenar las características de todos los archivos
all_audio_features = []
all_audio_names = []  # Lista para almacenar los nombres de los archivos
all_mel_spectrograms = []  # Lista para almacenar los espectrogramas

# Recorrer todos los archivos de audio en la carpeta
for root, dirs, files in os.walk(audio_folder):
    for file in files:
        if file.endswith(".mp3"):
            audio_file = os.path.join(root, file)
            print(f"Procesando: {audio_file}")

            # Extraer características del archivo de audio
            features = extract_audio_features(audio_file)

            # Cargar el espectrograma de Mel
            mel_spectrogram = np.load(audio_file.replace(".mp3", "_mel_spectrogram.npy"))

            all_audio_features.append(features)
            all_audio_names.append(file)
            all_mel_spectrograms.append(mel_spectrogram)

#Descomentar si se quieren ver cada espectrogramas por separado
# Visualizar el espectrograma después de procesar todos los archivos
# for root, dirs, files in os.walk(audio_folder):
#     for file in files:
#         if file.endswith(".mp3"):
#             audio_file = os.path.join(root, file)
#             mel_spectrogram = np.load(audio_file.replace(".mp3", "_mel_spectrogram.npy"))
#             plt.figure(figsize=(10, 4))
#             librosa.display.specshow(librosa.power_to_db(mel_spectrogram, ref=np.max), y_axis='mel',
#             x_axis='time')
#             plt.colorbar(format='%+2.0f dB')
#             plt.title(f'Mel Spectrogram - {file}')
#             plt.show()
#

# Visualizar todos los espectrogramas en una sola figura
plt.figure(figsize=(15, 10))

for i, mel_spectrogram in enumerate(all_mel_spectrograms):
    plt.subplot(len(all_mel_spectrograms), 1, i + 1)
    librosa.display.specshow(librosa.power_to_db(mel_spectrogram, ref=np.max), y_axis='mel', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Mel Spectrogram - {all_audio_names[i]}')

plt.tight_layout()
plt.show()