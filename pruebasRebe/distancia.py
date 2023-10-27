import pandas as pd
from scipy.spatial import distance

# Función para calcular la distancia euclidiana entre dos conjuntos de características
def euclidean_distance(features1, features2):
    return distance.euclidean(features1, features2)

# Cargar el DataFrame con las características de audio
features_df = pd.read_csv("audio_features_parecidos.csv")

# Crear una lista para almacenar las distancias
distances = []

# Calcular la distancia euclidiana entre pares de archivos
for i in range(len(features_df)):
    for j in range(i+1, len(features_df)):
        features1 = features_df.iloc[i][:13]  # Seleccionar las primeras 13 columnas (características)
        features2 = features_df.iloc[j][:13]  # para calcular la distancia
        dist = euclidean_distance(features1, features2)
        audio1 = features_df.iloc[i]['Nombre']
        audio2 = features_df.iloc[j]['Nombre']
        distances.append([audio1, audio2, dist])

# Crear un DataFrame para las distancias
distance_df = pd.DataFrame(distances, columns=['Audio1', 'Audio2', 'Distancia'])

# Guardar el DataFrame de distancias en un archivo CSV
distance_df.to_csv("audio_distances_parecidos.csv", index=False)
