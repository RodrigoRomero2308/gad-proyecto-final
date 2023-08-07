from pydub import AudioSegment
import os

def split_audio_by_canto(input_file, output_folder, canto_duration):
    # Cargar el archivo de audio
    audio = AudioSegment.from_mp3(input_file)

    # Definir la duración de los periodos de canto en milisegundos
    canto_duration_ms = canto_duration * 1000

    # Calcular la cantidad total de periodos de canto
    total_cantos = len(audio) // canto_duration_ms

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Cortar y guardar cada periodo de canto
    for canto_index in range(total_cantos):
        start_time = canto_index * canto_duration_ms
        end_time = start_time + canto_duration_ms

        canto = audio[start_time:end_time]

        output_file = os.path.join(output_folder, f"canto_{canto_index + 1}.mp3")
        canto.export(output_file, format="mp3")

    print(f"Se han creado {total_cantos} archivos de canto en la carpeta '{output_folder}'.")

# Ruta al archivo de audio de entrada (ajusta esto según tu caso)
input_audio_file = "canto_de_ave.mp3"

# Carpeta de salida para los cantos cortados (ajusta esto según tu caso)
output_cantos_folder = "cantos_cortados"

# Duración de cada periodo de canto en segundos
canto_duration_seconds = 10

split_audio_by_canto(input_audio_file, output_cantos_folder, canto_duration_seconds)