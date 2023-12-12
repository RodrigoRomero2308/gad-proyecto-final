from db import save_to_db, similarity_search

filepath = "C:/Users/rodri/OneDrive/Documentos/Facultad/GAD/aves/test2/XC17014.mp3"
species_common_name = "Black and white Warbler"
species_scientific_name= "mniotilta varia"


save_to_db(filepath, species_common_name, species_scientific_name)
# similarity_search(filepath)