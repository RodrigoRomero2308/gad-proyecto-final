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
BEGIN
	FOR i IN 1..10 LOOP
		if i=10 then
			bird_song_id_to_insert = new.id;
		end if;
		
		select vector into pivot_vector from pivot where pivot."level" = i;
		
		raise notice 'iteracion % pivote %', i, pivot_vector;
		
		distance_from_pivot := euclidean_distance(new.vector, pivot_vector);
		
		raise notice 'distancia del pivote %', distance_from_pivot;
		
		if parent_id_last_pivot is null then
			select * into tree_item from tree t 
			where t.parent_id is null and distance_from_pivot between t.lower_distance and t.upper_distance;
		else
			select * into tree_item from tree t 
			where t.parent_id = parent_id_last_pivot and distance_from_pivot between t.lower_distance and t.upper_distance;
		end if;
		
		if i < 10 then
			if tree_item.id is not null then
				parent_id_last_pivot:= tree_item.id;
				raise notice 'nuevo parent_id %', parent_id_last_pivot;
			else
				INSERT INTO tree (parent_id, vector_id, distancia)
				VALUES
					(parent_id_last_pivot, bird_song_id_to_insert, distance_from_pivot)
				returning id into parent_id_last_pivot;
				
				raise notice 'nuevo parent_id post insert %', parent_id_last_pivot;
			end if;
		else
			INSERT INTO tree (parent_id, vector_id, distancia)
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
BEGIN
	nodos_ultimo_nivel:='{}';
	FOR i IN 1..10 LOOP
		select vector into pivote from pivotes where nivel = i;
		
		distance_from_pivot:=euclidean_distance(vector_buscada, pivote);
		
		raise notice 'Distancia % con el pivote', distance_from_pivot;
		
		-- Busco todas las clases de este nivel que tengan distancia menor o igual a lo buscado 
		-- Deberian tener como padres los nodos encontrados en la ultima iteracion
		-- El resultado lo guardo
		
		select array_agg("id") into nodos_ultimo_nivel from tree
		where ABS(distancia - distance_from_pivot) <= radio
		AND  ((array_length(nodos_ultimo_nivel, 1) is null AND parent_id is null) 
			 OR
			  array_length(nodos_ultimo_nivel, 1) is not null AND parent_id = ANY(nodos_ultimo_nivel)
			 );
		
		raise notice 'Encontrados % elementos', nodos_ultimo_nivel;
	END LOOP;
	
	return query select 
		vector as vector_encontrada, 
		euclidean_distance(vector_buscada, vector) as distancia_con_vector from bird_song
	where euclidean_distance(vector_buscada, vector) <= radio
	AND "id" in (
		SELECT "vector_id" from tree
		where "id" = ANY(nodos_ultimo_nivel)
	);
END;
$busquedaFHQT$
language plpgsql;

CREATE OR REPLACE function "promedio_distancias_maximas"(pivotes varchar[], pares varchar[][]) RETURNS int as
$$
declare
	total int;
	distmax int;
	newdist int;
	par varchar[];
	pivote varchar;
begin
	total := 0;
	for i in 1..array_length(pares, 1) loop
		par := pares[i:i];
		distmax := 0;
		foreach pivote in array pivotes loop
			newdist := abs(levenshtein(pivote, unnest(par[1:1][1:1])) - levenshtein(pivote, unnest(par[1:1][2:2])));
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

CREATE OR REPLACE function "seleccionar_pivotes_incremental"() RETURNS varchar[] as
$$
DECLARE
	par VARCHAR[];
	pares varchar[][];
	paresaux varchar[][];
	pivotes VARCHAR[];
	candidatos VARCHAR[];
	actualresultado int;
	mejorresultado int;
	actualpivote varchar;
	mejorpivote varchar;
begin
	pares := '{}';
	for i in 1..80 loop
		par := array(select vector::varchar from bird_song order by random() limit 2);
		paresaux := array[par];
		pares := array_cat(pares, paresaux);
	end loop;
		
	pivotes := '{}';
	FOR i IN 1..7 loop
		candidatos := array(select vector::varchar from bird_song where not vector = any(pivotes) order by random() limit 10);
		mejorpivote := '';
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

select seleccionar_pivotes_incremental();