CREATE OR REPLACE FUNCTION euclidean_distance(l NUMERIC[], r NUMERIC[]) RETURNS NUMERIC AS $$
DECLARE
  s NUMERIC;
  vector_length INT;
BEGIN
  s := 0;
  vector_length := array_length(l, 1);
  FOR i IN 1..vector_length LOOP
    s := s + (l[i] - r[i]) ^ 2.0;
  END LOOP;
  RETURN |/ s;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE function "calcular_arbol_vector"() RETURNS TRIGGER AS
$build_tree$
DECLARE
	pivot_vector NUMERIC[];
	distance_from_pivot numeric;
	parent_id_last_pivot int;
	tree_item tree%rowtype;
	bird_song_id_to_insert int;
	levels int;
	rango range%rowtype;
BEGIN
	select max(level) into levels from pivot group by level limit 1;
	FOR i IN 1..levels LOOP
		if i=levels then
			bird_song_id_to_insert = new.id;
		end if;
		
		select vector into pivot_vector from pivot where pivot."level" = i;
		
		raise notice 'iteracion % pivote %', i, pivot_vector;
		
		distance_from_pivot := euclidean_distance(new.vector, pivot_vector);
		
		raise notice 'distancia del pivote %', distance_from_pivot;
		
		if parent_id_last_pivot is null then
			select * into tree_item from tree t 
			where t.parent_id is null and (distance_from_pivot between t.lower_distance and t.upper_distance
			or distance_from_pivot > t.lower_distance and t.upper_distance is null);
		else
			select * into tree_item from tree t 
			where t.parent_id = parent_id_last_pivot and (distance_from_pivot between t.lower_distance and t.upper_distance
			or distance_from_pivot > t.lower_distance and t.upper_distance is null);
		end if;
		
		if i < levels then
			if tree_item.id is not null then
				parent_id_last_pivot:= tree_item.id;
				raise notice 'nuevo parent_id %', parent_id_last_pivot;
			else
				select * into rango from "range" r where (distance_from_pivot between r.lower_distance and r.upper_distance
					or distance_from_pivot > r.lower_distance and r.upper_distance is null);
				INSERT INTO tree (parent_id, level, lower_distance, upper_distance)
				VALUES
					(parent_id_last_pivot, i, rango.lower_distance, rango.upper_distance)
				returning id into parent_id_last_pivot;
				
				raise notice 'nuevo parent_id post insert %', parent_id_last_pivot;
			end if;
		else
			INSERT INTO tree (parent_id, bird_song_id, level, lower_distance, upper_distance)
				VALUES
					(parent_id_last_pivot, bird_song_id_to_insert, levels, distance_from_pivot, null);
			
			raise notice 'Inserto nodo hoja';
		end if;
	raise notice 'vector %, iteracion %, parent %', new.vector, i, parent_id_last_pivot;
	END LOOP;
	
	return new;
END;
$build_tree$
language plpgsql;

CREATE OR REPLACE FUNCTION busquedaFHQT(vector_buscada NUMERIC[], radio NUMERIC) returns TABLE (
	result_id int,
	vector_encontrada NUMERIC[],
	distancia_con_vector NUMERIC
) as
$busquedaFHQT$
DECLARE
	pivote NUMERIC[];
	distance_from_pivot NUMERIC;
	nodos_ultimo_nivel INT ARRAY;
	levels int;
BEGIN
	select max(level) into levels from pivot group by level limit 1;
	nodos_ultimo_nivel:='{}';
	FOR i IN 1..levels LOOP
		select vector into pivote from pivot where level = i;
		
		distance_from_pivot:=euclidean_distance(vector_buscada, pivote);
		
		raise notice 'Distancia % con el pivote', distance_from_pivot;
		
		-- Busco todas las clases de este nivel que tengan distancia menor o igual a lo buscado 
		-- Deberian tener como padres los nodos encontrados en la ultima iteracion
		-- El resultado lo guardo
		
		select array_agg("id") into nodos_ultimo_nivel from tree
		where ABS(lower_distance - distance_from_pivot) <= radio
		AND  ((array_length(nodos_ultimo_nivel, 1) is null AND parent_id is null) 
			 OR
			  array_length(nodos_ultimo_nivel, 1) is not null AND parent_id = ANY(nodos_ultimo_nivel)
			 );
		
		raise notice 'Encontrados % elementos', nodos_ultimo_nivel;
	END LOOP;
	
	return query select 
		"id" as result_id,
		vector as vector_encontrada, 
		euclidean_distance(vector_buscada, vector) as distancia_con_vector from bird_song
	where euclidean_distance(vector_buscada, vector) <= radio
	AND "id" in (
		SELECT "bird_song_id" from tree
		where "id" = ANY(nodos_ultimo_nivel)
	); -- revisar explain para que filtro de id se haga primero
END;
$busquedaFHQT$
language plpgsql;

CREATE OR REPLACE function "promedio_distancias_maximas"(pivotes arraydos[], pares arraytres[]) RETURNS numeric as
$$
declare
	total numeric;
	distmax numeric;
	newdist numeric;
	par arraydos[];
begin
	total := 0;
	for i in 1..array_length(pares, 1) loop
		par := pares[i].arr;
		distmax := 0;
		for j in 1..array_length(pivotes, 1) loop
			newdist := abs(euclidean_distance(pivotes[j].arr, (par[1]).arr) - euclidean_distance(pivotes[j].arr, (par[2]).arr));
			if newdist > distmax then
				distmax := newdist;
			end if;
		end loop;
		total := total + distmax;
	end loop;
	return total / array_length(pares, 1);
END;
$$
language plpgsql;

CREATE OR REPLACE function "seleccionar_pivotes_incremental"(cantidad int) RETURNS arraydos[] as
$$
DECLARE
	par arraytres;
	pares arraytres[];
	pivotes arraydos[];
	candidatos arraydos[];
	actualresultado numeric;
	mejorresultado numeric;
	actualpivote arraydos;
	mejorpivote arraydos;
begin
	pares := array[]::arraytres[];
	for i in 1..80 loop
		par := row((select array(select row(vector)::arraydos from bird_song order by random() limit 2)::arraydos[])::arraydos[]);
		pares := array_append(pares, par);
	end loop;
		
	pivotes := ARRAY[]::arraydos[];
	FOR i IN 1..cantidad loop
		candidatos := array(select row(vector)::arraydos from bird_song order by random() limit 10)::arraydos[];
		mejorpivote := row((select array[]::numeric[]));
		mejorresultado := 0;
		for j in 1..10 loop
			actualpivote := candidatos[j];
			actualresultado := promedio_distancias_maximas(array_append(pivotes, actualpivote), pares);
			if mejorresultado < actualresultado then
				mejorpivote := actualpivote;
				mejorresultado := actualresultado;
			end if;
		end loop;
		raise notice 'pivotes %', pivotes;
		raise notice 'mejorpivote %', mejorpivote;
		pivotes := array_append(pivotes, mejorpivote);
	END LOOP;
	raise notice 'pivoteslength %', array_length(pivotes, 1);
	return pivotes;
END;
$$
language plpgsql;

CREATE OR REPLACE FUNCTION "insertar_rangos_entre_pivotes"() RETURNS void AS
$insertar_rangos_entre_pivotes$
DECLARE
	pivotes arraydos[];
	pivote arraydos;
	pivote2 arraydos;
	highest_distance NUMERIC;
	new_distance NUMERIC;
	range_increment NUMERIC;
	nivel int;
	cantidad_rangos int;
BEGIN
	DELETE FROM "tree";
	DELETE FROM "pivot";
	DELETE FROM "range";

	highest_distance := 0;
	nivel := 0;
	cantidad_rangos := 8;
	pivotes := seleccionar_pivotes_incremental(10);

	foreach pivote in array pivotes loop
		nivel := nivel + 1;
		INSERT INTO pivot (vector, level)
			VALUES (pivote.arr, nivel);

		foreach pivote2 in array pivotes loop
			new_distance := euclidean_distance(pivote.arr, pivote2.arr);
			if new_distance > highest_distance then
				highest_distance := new_distance;
			end if;
		end loop;
	end loop;

	range_increment := highest_distance / nivel;

	for i in 1..cantidad_rangos loop
		if i = cantidad_rangos then
			INSERT INTO "range" (lower_distance, upper_distance)
				VALUES (range_increment * (i - 1), null);
		else
			INSERT INTO "range" (lower_distance, upper_distance)
				VALUES (range_increment * (i - 1), range_increment * i);
		end if;
	end loop;
END;
$insertar_rangos_entre_pivotes$
language plpgsql;

CREATE OR REPLACE function "recargar_arbol"() RETURNS void AS
$recargar_arbol_item$
DECLARE
	pivot_vector NUMERIC[];
	distance_from_pivot NUMERIC;
	parent_id_last_pivot int;
	tree_item tree%rowtype;
	bird_song_id_to_insert int;
	levels int;
	rango range%rowtype;
	song bird_song%rowtype;
begin
	DELETE FROM "tree";
	
	select max(level) into levels from pivot group by level limit 1;
	for song in (select * from bird_song) loop
		parent_id_last_pivot := null;
		bird_song_id_to_insert := null;
		FOR i IN 1..levels LOOP
			if i=levels then
				bird_song_id_to_insert = song.id;
			end if;
			
			select vector into pivot_vector from pivot where pivot."level" = i;
			
			raise notice 'iteracion % pivote %', i, pivot_vector;
			
			distance_from_pivot := euclidean_distance(song.vector, pivot_vector);
			
			raise notice 'distancia del pivote %', distance_from_pivot;
			
			if parent_id_last_pivot is null then
				select * into tree_item from tree t 
				where t.parent_id is null and (distance_from_pivot between t.lower_distance and t.upper_distance
				or distance_from_pivot > t.lower_distance and t.upper_distance is null);
			else
				select * into tree_item from tree t 
				where t.parent_id = parent_id_last_pivot and (distance_from_pivot between t.lower_distance and t.upper_distance
				or distance_from_pivot > t.lower_distance and t.upper_distance is null);
			end if;
			
			if i < levels then
				if tree_item.id is not null then
					parent_id_last_pivot:= tree_item.id;
					raise notice 'nuevo parent_id %', parent_id_last_pivot;
				else
					select * into rango from "range" r where (distance_from_pivot between r.lower_distance and r.upper_distance
						or distance_from_pivot > r.lower_distance and r.upper_distance is null);
					INSERT INTO tree (parent_id, level, lower_distance, upper_distance)
					VALUES
						(parent_id_last_pivot, i, rango.lower_distance, rango.upper_distance)
					returning id into parent_id_last_pivot;
					
					raise notice 'nuevo parent_id post insert %', parent_id_last_pivot;
				end if;
			else
				INSERT INTO tree (parent_id, bird_song_id, level, lower_distance, upper_distance)
					VALUES
						(parent_id_last_pivot, bird_song_id_to_insert, levels, distance_from_pivot, null);
				
				raise notice 'Inserto nodo hoja';
			end if;
		raise notice 'vector %, iteracion %, parent %', song.vector, i, parent_id_last_pivot;
		END LOOP;
	end loop;
END;
$recargar_arbol_item$
language plpgsql;

--select insertar_rangos_entre_pivotes();
--select recargar_arbol();

-- CREATE OR REPLACE TRIGGER "calcular_arbol_vector" AFTER INSERT /* OR UPDATE OR DELETE */ ON bird_song for each row
-- execute procedure "calcular_arbol_vector"();