select b."id", b.filename, b.filepath, s.common_name, s.scientific_name, bf.* 
from busquedafhqt((select vector from bird_song order by id asc limit 1), 0.5) bf --cambiar el vector a gusto
inner join bird_song b on b."id" = bf."result_id"
inner join species s on b.species_id = s."id";

-- Eliminar cantos de prueba modificados

delete from tree
where bird_song_id in (
	select id from bird_song
	where fileurl like '%-4%' and fileurl not like '%X%'
);

delete from bird_song
where fileurl like '%-4%' and fileurl not like '%X%';

-- Change files URL

UPDATE bird_song
SET fileurl = REPLACE(fileurl, 'http://example.com/songs/', 'https://new-server.com/audio/');