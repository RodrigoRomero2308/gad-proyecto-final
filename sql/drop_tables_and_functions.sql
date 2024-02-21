DROP FUNCTION recargar_arbol();
DROP FUNCTION insertar_rangos_entre_pivotes();
DROP FUNCTION seleccionar_pivotes_incremental(cantidad int);
DROP FUNCTION promedio_distancias_maximas(pivotes arraydos[], pares arraytres[]);
DROP FUNCTION busquedaFHQT(vector_buscada NUMERIC[], radio NUMERIC);
DROP TRIGGER "calcular_arbol_vector" ON bird_song;
DROP FUNCTION calcular_arbol_vector();
DROP FUNCTION euclidean_distance(l NUMERIC[], r NUMERIC[]);

DROP TABLE "range";
DROP TYPE arraytres;
DROP TYPE arraydos;

DROP TABLE "tree";
DROP TABLE "pivot";
DROP TABLE "bird_song";
DROP TABLE "species";