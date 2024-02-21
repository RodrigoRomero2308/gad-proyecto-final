select b."id", b.filename, b.filepath, s.common_name, s.scientific_name, bf.* 
from busquedafhqt((select vector from bird_song order by id asc limit 1), 0.5) bf --cambiar el vector a gusto
inner join bird_song b on b."id" = bf."result_id"
inner join species s on b.species_id = s."id";