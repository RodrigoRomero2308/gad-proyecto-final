import os
from os import environ
from dotenv import load_dotenv
from embeddings import embed_audio
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from typing import Union
from models import BirdSong, Species

load_dotenv()

db_url = environ.get('DB_URL')

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)

def save_to_db(filepath: str, species_common_name: Union[str, None], species_scientific_name: Union[str, None]):
  if not os.path.exists(filepath):
    raise FileNotFoundError()
  
  filename = os.path.basename(filepath)

  file_embeddings = embed_audio(filepath)

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

  # FIXME: file_embeddings es de tipo ndarray, da error: psycopg2.ProgrammingError: can't adapt type 'numpy.ndarray'
  new_bird_song = BirdSong(filename=filename, vector=file_embeddings)

  session.add(new_bird_song)
  session.commit()

  print(new_bird_song)

  # Cerramos la sesion
  session.close()
  return

def similarity_search(filepath: str):
  if not os.path.exists(filepath):
    raise FileNotFoundError()

  file_embeddings = embed_audio(filepath)

  # Buscamos en postgres llamando a la funcion necesaria