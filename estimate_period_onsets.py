import os
import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import shutil

def get_most_constant_onset_span(spans: list):
    lowest_difference = np.Infinity
    lowest_difference_index = -1
    for span_index in range(spans.__len__() - 1):
        difference = float(abs(spans[span_index] - spans[span_index + 1]))
        if difference < lowest_difference:
            lowest_difference = difference
            lowest_difference_index = span_index
    return lowest_difference_index, lowest_difference

def process_audio_file(filename: str, folder: str):
    filename_without_extension, extension = os.path.splitext(filename)
    this_file_dir = f'output/{filename_without_extension}'
    os.makedirs(this_file_dir)

    shutil.copy(f'{folder}/{filename}', f'{this_file_dir}/original.{extension}')
    
    y, sr = librosa.load(f'{folder}/{filename}')

    # Calcular la función de envolvente de inicio
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Detectar los onsets (inicios de eventos)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, backtrack=True)

    # Convertir los onsets a tiempos en segundos
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # Visualizar los onsets en el espectrograma
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(librosa.amplitude_to_db(librosa.stft(y), ref=np.max),
                            x_axis='time', y_axis='log')
    plt.vlines(onset_times, 0, sr/2, color='r', linestyle='--', label='Onsets')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma con Onsets')
    # plt.show()
    plt.savefig(f'{this_file_dir}/espectrograma_onsets.png', bbox_inches='tight', pad_inches=0.0)

    print(onset_times)

    onset_times_spans = []

    for index in range(onset_times.__len__() - 1):
        element = onset_times[index]
        next_element = onset_times[index + 1]
        onset_times_spans.append(next_element - element)

    lowest_difference_span_index, difference = get_most_constant_onset_span(onset_times_spans)

    start_sample = int(onset_times[lowest_difference_span_index] * sr)
    end_sample = int(onset_times[lowest_difference_span_index + 1] * sr)

    sf.write(f'{this_file_dir}/periodo.wav', y[start_sample:end_sample], sr)

# Ruta a carpeta con los mp3 a procesar
folder_with_media_files = 'C:/Users/rodri/OneDrive/Documentos/Facultad/GAD/aves/test_media'

# Descomentar si se quiere borrar todo el output anterior
# if os.path.exists('output'):
#     shutil.rmtree('output')

# Obtener los nombres de todos los archivos en el directorio
file_names = os.listdir(folder_with_media_files)

# Filtrar solo los nombres de archivos (excluyendo carpetas)
file_names = [file_name for file_name in file_names if os.path.isfile(os.path.join(folder_with_media_files, file_name))]

for file_name in file_names:
    file_name_wothout_extension = os.path.splitext(file_name)[0]
    if (os.path.exists(f'output/{file_name_wothout_extension}')):
        continue
    process_audio_file(file_name, folder_with_media_files)
    