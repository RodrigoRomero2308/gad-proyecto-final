import os
import eyed3
from db import save_to_db

folderpath = 'C:/Users/rodri/OneDrive/Documentos/Facultad/GAD/50-query-set/upload'

# Asumiendo que la carpeta tiene la estructura enviada:
# - Cada subcarpeta representa los audios de una especie
# - Cada audio en la subcarpeta es un archivo .mp3 donde el titulo en sus metadatos contiene el nombre de la especie acompañado del nombre cientifico entre parentesis


def get_information_from_tag_title(title: str):
  [normal_name, scientific_name] = title.split(" (") # partimos segun el parentesis
  scientific_name = scientific_name[:-1] # eliminamos el parentesis que cierra
  return {"normal_name": normal_name, "scientific_name": scientific_name}


for folder_name, subfolders, filenames in os.walk(folderpath):
  for subfolder in subfolders:
    for child_folder_name, child_subfolders, child_filenames in os.walk(os.path.join(folder_name, subfolder)):
      for filename in child_filenames:
        fullfilePath = os.path.join(folder_name, subfolder, filename)
        filePath = f"{subfolder}/{filename}"
        mp3_file = eyed3.load(fullfilePath)
        tag = mp3_file.tag
        duration = mp3_file.info.time_secs
        if duration < 0.4:
          print(f"Skipping {filename}. Duration: {duration}")
          continue
        print(duration)
        title_info = get_information_from_tag_title(tag.title)
        save_to_db(fullfilePath, filePath, title_info["normal_name"], title_info["scientific_name"])


      
