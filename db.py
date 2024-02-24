import os
from os import environ
from dotenv import load_dotenv
from embeddings import embed_audio
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
from typing import Union
from models import BirdSong, Species

load_dotenv()

db_url = environ.get('DB_URL')
github_songs_folder = environ.get("GITHUB_SONGS_FOLDER")

print(github_songs_folder)

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)

def save_to_db(fullfilepath: str, urlFilePath: str, species_common_name: Union[str, None], species_scientific_name: Union[str, None]):
  if not os.path.exists(fullfilepath):
    raise FileNotFoundError()
  
  fileurl = github_songs_folder + "/" + urlFilePath

  file_embeddings = embed_audio(fullfilepath)

  # Buscamos la especie, si no existe la guardamos

  session = Session()

  species_select = select(Species).where(Species.common_name == species_common_name).where(Species.scientific_name == species_scientific_name)

  species = session.scalars(species_select).first()

  print(species)

  if species is None:
    new_species = Species(common_name=species_common_name, scientific_name=species_scientific_name)

    session.add(new_species)
    session.commit()

    species = session.scalars(species_select).first()

    print("Post creation")
    print(species)
  # Guardamos en la base

  new_bird_song = BirdSong(fileurl=fileurl, vector=file_embeddings, species_id=species.id)

  session.add(new_bird_song)
  session.commit()

  print(new_bird_song)

  # Cerramos la sesion
  session.close()
  return

def similarity_search(filepath: str, radius: int):
  if not os.path.exists(filepath):
    raise FileNotFoundError()

  file_embeddings = embed_audio(filepath)

  array_string = ", ".join([str(x) for x in file_embeddings])

  # Buscamos en postgres llamando a la funcion necesaria
  sql = text(f"""
select b."id", b.fileurl, s.common_name, s.scientific_name, bf.distancia_con_vector 
from busquedafhqt(ARRAY[{array_string}], {radius}) bf
inner join bird_song b on b."id" = bf."result_id"
inner join species s on b.species_id = s."id"
where bf.distancia_con_vector > 0
order by bf.distancia_con_vector asc
limit 10;
""")

  session = Session()

  result = session.execute(statement=sql)

  final_answer = []

  for row in result:
      final_answer.append({
        "id": row.id,
        "fileurl": row.fileurl,
        "common_name": row.common_name,
        "scientific_name": row.scientific_name,
        "distancia_con_vector": row.distancia_con_vector,
      })
  
  return final_answer