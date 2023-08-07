import numpy as np
import matplotlib.pyplot as plt
import librosa

# Cargar el archivo de audio
input_audio_file = "canto_de_ave.mp3"
y, sr = librosa.load(input_audio_file)

# Calcular la Transformada de Fourier
fft = np.fft.fft(y)
freqs = np.fft.fftfreq(len(y), 1/sr)

# Calcular las amplitudes de las frecuencias
amplitudes = np.abs(fft)

# Filtrar las frecuencias por un umbral de amplitud
threshold = np.max(amplitudes) * 0.1
filtered_freqs = freqs[amplitudes > threshold]

# Mostrar las frecuencias dominantes
print("Frecuencias dominantes:")
for freq in filtered_freqs:
    print(f"{freq:.2f} Hz")

# Visualizar el espectro de frecuencia
plt.figure(figsize=(10, 6))
plt.plot(freqs, amplitudes)
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.title("Espectro de Frecuencia")
plt.xlim(0, 5000)  # Limitar el rango para una mejor visualización
plt.show()