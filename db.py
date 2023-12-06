import os

from embeddings import embed_audio

def save_to_db(filepath: str):
  if not os.path.exists(filepath):
    raise FileNotFoundError()
  
  filename = os.path.basename(filepath)

  file_embeddings = embed_audio(filepath)

  # Guardamos en la base

  return

def similarity_search(filepath: str):
  if not os.path.exists(filepath):
    raise FileNotFoundError()

  file_embeddings = embed_audio(filepath)

  # Buscamos en postgres llamando a la funcion necesaria