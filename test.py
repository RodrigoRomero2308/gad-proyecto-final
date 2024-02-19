from embeddings import embed_audio


filepath = "C:/Users/rodri/OneDrive/Documentos/Facultad/GAD/aves/100cantos/100/Alder flycatcher/XC16965.mp3"

embeddings = embed_audio(filepath)

print(embeddings)
print(type(embeddings))