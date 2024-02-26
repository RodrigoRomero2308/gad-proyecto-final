from db import similarity_search

folderpath = 'C:/Users/rodri/OneDrive/Documentos/Facultad/GAD/50-query-set/50-query-set'
radius = 0.8 # Query is limited to 10 results anyways

successes5 = [0, 0, 0, 0, 0]
successes = [0, 0, 0, 0, 0]
anysuccesses = 0

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
        if str(file + 1) + "-" + str(1) + ".mp3" in result[i]["fileurl"]:
            for j in range(i, 5):
                successes5[j] = successes5[j] + 1
        if str(file + 1) + "-" + str(i + 1) + ".mp3" in result[i]["fileurl"]:
            successes[i] = successes[i] + 1
        if str(file + 1) + "-" in result[i]["fileurl"]:
            anysuccesses = anysuccesses + 1

print(f"Looking for the closest audio:")
print(f"First place success rate: {str(successes5[0] / 50 * 100)}%")
print(f"First 2 places success rate: {str(successes5[1] / 50 * 100)}%")
print(f"First 3 places success rate: {str(successes5[2] / 50 * 100)}%")
print(f"First 4 places success rate: {str(successes5[3] / 50 * 100)}%")
print(f"First 5 places success rate: {str(successes5[4] / 50 * 100)}%")
print(f"Looking for the 5 closest audios:")
print(f"General ordered success rate: {str(sum(successes) / 250 * 100)}%")
print(f"Flexive success rate: {str(anysuccesses / 250 * 100)}%")
print(f"1st audio in 1st place: {str(successes[0] / 50 * 100)}%")
print(f"2nd audio in 2nd place: {str(successes[1] / 50 * 100)}%")
print(f"3rd audio in 3rd place: {str(successes[2] / 50 * 100)}%")
print(f"4th audio in 4th place: {str(successes[3] / 50 * 100)}%")
print(f"5th audio in 5th place: {str(successes[4] / 50 * 100)}%")