CREATE OR REPLACE FUNCTION euclidean_distance(l NUMERIC[], r NUMERIC[]) RETURNS NUMERIC AS $$
DECLARE
  s NUMERIC;
  vector_length INT;
BEGIN
  s := 0;
  vector_length := array_length(l);
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
	distance_from_pivot int;
	parent_id_last_pivot int;
	tree_item tree%rowtype;
	bird_song_id_to_insert int;
	levels int;
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
			parent_id_last_pivot:= tree_item.id;
			raise notice 'nuevo parent_id %', parent_id_last_pivot;
		else
			INSERT INTO tree (parent_id, vector_id, lower_distance)
				VALUES
					(parent_id_last_pivot, bird_song_id_to_insert, distance_from_pivot);
			
			raise notice 'Inserto nodo hoja';
		end if;
	raise notice 'vector %, iteracion %, parent %', new.vector, i, parent_id_last_pivot;
	END LOOP;
	
	return new;
END;
$build_tree$
language plpgsql;

CREATE OR REPLACE TRIGGER "calcular_arbol_vector" AFTER INSERT /* OR UPDATE OR DELETE */ ON bird_song for each row
execute procedure "calcular_arbol_vector"();

CREATE OR REPLACE FUNCTION busquedaFHQT(vector_buscada NUMERIC[], radio int) returns TABLE (
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
		"id",
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

CREATE OR REPLACE function "promedio_distancias_maximas"(pivotes numeric[][], pares numeric[][][]) RETURNS numeric as
$$
declare
	total numeric;
	distmax numeric;
	newdist numeric;
	par numeric[][];
	pivote numeric[];
begin
	total := 0;
	for i in 1..array_length(pares, 1) loop
		par := pares[i:i];
		distmax := 0;
		foreach pivote in array pivotes loop
			newdist := abs(euclidean_distance(pivote, unnest(par[1:1][1:1])) - euclidean_distance(pivote, unnest(par[1:1][2:2])));
			--raise notice '% % %', newdist, pivote, par;
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

CREATE OR REPLACE function "seleccionar_pivotes_incremental"() RETURNS numeric[][] as
$$
DECLARE
	par numeric[][];
	pares numeric[][][];
	paresaux numeric[][][];
	pivotes numeric[][];
	candidatos numeric[][];
	actualresultado numeric;
	mejorresultado numeric;
	actualpivote numeric[];
	mejorpivote numeric[];
begin
	pares := '{}';
	for i in 1..80 loop
		par := array(select vector from bird_song order by random() limit 2);
		paresaux := array[par];
		pares := array_cat(pares, paresaux);
	end loop;
		
	pivotes := '{}';
	FOR i IN 1..10 loop
		candidatos := array(select vector from bird_song where not vector = any(pivotes) order by random() limit 10);
		mejorpivote := '{}';
		mejorresultado := 0;
		for j in 1..10 loop
			actualpivote := candidatos[j];
			actualresultado := promedio_distancias_maximas( array_append(pivotes, actualpivote), pares);
			--raise notice '%', actualresultado;
			if mejorresultado < actualresultado then
				mejorpivote := actualpivote;
				mejorresultado := actualresultado;
			end if;
		end loop;
		pivotes := array_append(pivotes, mejorpivote);
	END LOOP;
	return pivotes;
END;
$$
language plpgsql;

CREATE OR REPLACE FUNCTION "insertar_rangos_entre_pivotes"() RETURNS void AS
$insertar_rangos_entre_pivotes$
DECLARE
	pivotes NUMERIC[][];
	pivot_vector NUMERIC[];
	highest_distance NUMERIC;
	new_distance NUMERIC;
	range_increment NUMERIC;
	nivel int;
	cantidad_rangos int;
	parent_ids int[];
BEGIN
	DELETE FROM "tree";
	DELETE FROM "pivot";

	highest_distance := 0;
	nivel := 0;
	cantidad_rangos := 10;
	pivotes := seleccionar_pivotes_incremental();

	foreach pivote in array pivotes loop
		nivel := nivel + 1;
		INSERT INTO pivot (vector, level)
			VALUES (pivote, nivel);

		foreach pivote2 in array pivotes loop
			new_distance := euclidean_distance(pivote, pivote2);
			if new_distance > highest_distance then
				highest_distance := new_distance;
			end if;
		end loop;
	end loop;

	new_distance := 0;
	range_increment := highest_distance / nivel; --pasar int a numeric

	--Por cada nivel (cant de pivotes)
	FOR i IN 1..nivel LOOP
		select array_agg(id) into parent_ids from tree where level = (i - 1);
		--Por la cantidad de rangos
		FOR j IN 1..cantidad_rangos LOOP
			--Si es el primer nivel no lleva parent_id
			if i == 1 then
				--Si es el último rango no tiene upper_distance
				if j == cantidad_rangos then
					INSERT INTO tree (parent_id, level, lower_distance, upper_distance)
						VALUES (null, i, range_increment * (j - 1), null);
				else
					INSERT INTO tree (parent_id, level, lower_distance, upper_distance)
						VALUES (null, i, range_increment * (j - 1), range_increment * j)
				end if;
			--Si es otro nivel hay buscar los nodos que tengan nivel i - 1 y para cada uno insertar el rango j
			else
				foreach p_id in array parent_ids loop
					--Si es el último rango no tiene upper_distance
					if j == (nivel - 1) then
						INSERT INTO tree (parent_id, level, lower_distance, upper_distance)
							VALUES (p_id, i, range_increment * (j - 1), null);
					else
						INSERT INTO tree (parent_id, level, lower_distance, upper_distance)
							VALUES (p_id, i, range_increment * (j - 1), range_increment * j)
					end if;
				end loop;
			end if;
		end loop;
	end loop;
END;
$insertar_rangos_entre_pivotes$
language plpgsql;

CREATE OR REPLACE function "recargar_arbol_item"(neww bird_song%rowtype) RETURNS void AS
$recargar_arbol_item$
DECLARE
	pivot_vector NUMERIC[];
	distance_from_pivot int;
	parent_id_last_pivot int;
	tree_item tree%rowtype;
	bird_song_id_to_insert int;
	levels int;
BEGIN
	select max(level) into levels from pivot group by level limit 1;
	FOR i IN 1..levels LOOP
		if i=levels then
			bird_song_id_to_insert = neww.id;
		end if;
		
		select vector into pivot_vector from pivot where pivot."level" = i;
		
		raise notice 'iteracion % pivote %', i, pivot_vector;
		
		distance_from_pivot := euclidean_distance(neww.vector, pivot_vector);
		
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
			parent_id_last_pivot:= tree_item.id;
			raise notice 'nuevo parent_id %', parent_id_last_pivot;
		else
			INSERT INTO tree (parent_id, vector_id, lower_distance)
				VALUES
					(parent_id_last_pivot, bird_song_id_to_insert, distance_from_pivot);
			
			raise notice 'Inserto nodo hoja';
		end if;
	raise notice 'vector %, iteracion %, parent %', neww.vector, i, parent_id_last_pivot;
	END LOOP;
END;
$recargar_arbol_item$
language plpgsql;

CREATE OR REPLACE function "recargar_arbol"() RETURNS void AS
$recargar_arbol_item$
DECLARE
	song bird_song%rowtype;
BEGIN
	foreach song in (select * from bird_song) loop
		recargar_arbol_item(song);
	end loop;
END;
$recargar_arbol_item$
language plpgsql;

--select insertar_rangos_entre_pivotes();
