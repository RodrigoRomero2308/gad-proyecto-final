# TODO

- Crear el algoritmo para calcular el indice FHQT+ (no incluye el vector representativo, siempre lo vamos a calcular por python) (Rebe)
- Base de datos: funcion de busqueda, parametro: vector caracteristico, radio. salida: ids y distancia de los mas parecidos (maximo 10) (Luisi)
- Hacer una funcion que reciba como parametro un path (de un archivo de audio), obtenga el vector representativo (con el otro archivo) y busque en la base de datos los audios "mas cercanos" (ver parametros) (RR)
- Postgres: seleccion de pivotes por seleccion incremental (capaz que no)
- Definir lote de 50 consultas, resultado esperado, % de aciertos a la primera y en 5 lugares

## Innecesarios

- Interfaz visual (Rorro)
- Repositorio de archivos (links de audios)

# Done

- Un archivo con una funcion que reciba como parametro un path a un audio y calcule el vector de numeros que lo represente (Coeficientes septrales de mel) (done)
- Definir schema de base de datos postgres para guardar (nombre de archivo, vector representativo) + todas las tablas necesarias para FHQT (done)
- Un archivo con una funcion que reciba como parametro un path, un nombre de archivo y una lista de numeros y los guarde en una base de datos (done)
- Buscar repositorio de audios (con 100 alcanza como para probar) (done)