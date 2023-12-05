import os
import pandas

from finalcode.embeddings import embed_audio


folder = 'C:\\Users\\rodri\\OneDrive\\Documentos\\Facultad\\GAD\\Code\\audios\\parecidos'

files_in_folder = os.listdir(folder)

document_data = []

for file in files_in_folder:
  if not file.endswith('.wav'):
    continue

  embeddings = embed_audio(os.path.join(folder, file))

  document_data.append({
    "filename": file,
    "embeddings": embeddings,
  })

  