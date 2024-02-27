from db import similarity_search

folderpath = 'C:/Users/rodri/OneDrive/Documentos/Facultad/GAD/50/50'
radius = 0.8 # Query is limited to 10 results anyways

successes5 = [0, 0, 0, 0, 0]

audios_processed = 0

def save_results(filename, results):
    with open(f"results/{filename}.txt", 'w') as file:
        for result in results:
            fileurl = result["fileurl"]
            distancia_con_vector = result["distancia_con_vector"]
            file.write(f"{fileurl}. Distancia {distancia_con_vector}\n")

for file in range(50):
    print(f"Procesando {file + 1}.mp3")
    full_file_path = folderpath + "/" + str(file + 1) + ".mp3"
    result: list = similarity_search(full_file_path, radius, 5)
    print(f"Encontrados {result.__len__()} resultados")
    save_results(f"{file + 1}.mp3", result)
    audios_processed = audios_processed + 1
    print(f"Procesados {audios_processed} audios")
    for i in range(5):
        if str(file + 1) + "-" + str(5) + ".mp3" in result[i]["fileurl"]:
            for j in range(i, 5):
                successes5[j] = successes5[j] + 1

print(f"Looking for the closest audio:")
print(f"First place success rate: {str(successes5[0] / 50 * 100)}%")
print(f"First 2 places success rate: {str(successes5[1] / 50 * 100)}%")
print(f"First 3 places success rate: {str(successes5[2] / 50 * 100)}%")
print(f"First 4 places success rate: {str(successes5[3] / 50 * 100)}%")
print(f"First 5 places success rate: {str(successes5[4] / 50 * 100)}%")