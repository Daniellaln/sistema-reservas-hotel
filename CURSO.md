# Aplicación de Estructura de Datos y Algoritmos

## Qué se implementa

| Tema | Archivo | Operación real |
| --- | --- | --- |
| Clases y nodos | estructuras.py | nodo con dato, izq y der |
| Listas de Python | modelo.py | entidades del hotel |
| Lista simplemente enlazada | estructuras.py | nodos de la cola de espera |
| Cola FIFO | estructuras.py | encolar al final, desencolar al inicio |
| Lista doblemente enlazada | estructuras.py | historial, recorridos en ambos sentidos |
| Árbol binario de búsqueda | estructuras.py | huéspedes indexados por DNI |
| Recursión | algoritmos.py | división de Merge Sort |
| Ordenamiento | algoritmos.py | Merge Sort estable por fecha o importe |
| Búsqueda lineal | modelo.py | habitaciones y reservas |
| Excepciones | modelo.py, repositorio.py | datos inválidos, archivo corrupto, fallo de escritura |
| Almacenamiento en disco | repositorio.py | JSON, archivo temporal y copia previa |

No se implementan AVL, grafos, heaps, backtracking ni pila propia. El recorrido inorden del árbol usa una lista de Python como pila auxiliar, sin presentarla como una estructura propia. No es necesario usar todas las unidades; confirmar con la rúbrica del profesor cuántas estructuras exige el proyecto.

## Complejidad

- Cola: encolar y desencolar O(1). Convertir a lista para guardar: O(n).
- Lista doble: agregar al final O(1); recorrido O(n).
- Árbol normal: insertar y buscar O(h), peor caso O(n) si se desequilibra. No se promete O(log n).
- Merge Sort: O(n log n), espacio auxiliar O(n). Conserva el orden de elementos con igual fecha o importe.
- Disponibilidad: búsqueda de habitación y recorrido de reservas O(H + R).
- Saldo: recorrer pagos O(P).
- Guardado: serializa todos los datos y valida su integridad. La comprobación de solapamientos importados es O(R²) y saldos O(R·P), además de búsquedas. Para este prototipo pequeño es aceptable; no es una arquitectura de hotel grande.
- Consultar estado calcula saldos de cada reserva O(R·P), además de Merge Sort y búsquedas.

## Pseudocódigo del solapamiento

```
buscar habitación
si no existe o está en mantenimiento: no disponible
para cada reserva activa de esa habitación:
    si nueva entrada < salida existente Y nueva salida > entrada existente:
        no disponible
disponible
```

## Pseudocódigo de Merge Sort

```
si la lista tiene cero o un elemento: devolver copia
dividir por la mitad
ordenar recursivamente cada mitad
mezclar comparando las claves
en un empate, tomar primero el elemento izquierdo
devolver la lista ordenada
```

## Sustentación sugerida

Mostrar primero estructuras.py y sus nodos. Demostrar dos solicitudes en espera y atender la primera. Invertir el historial. Buscar un DNI exacto con el botón de búsqueda en árbol. Ordenar la agenda por llegada y por importe; el puente usa merge_sort, no sorted. Mostrar algoritmos.py. Registrar pago parcial, intentar sobrepago y cobrar el resto antes del check-out. Exportar JSON y reiniciar para demostrar persistencia.

Los nombres chu.lon y soy.leona son guiños internos: cuenta.lon suma pagos y calendario.leona comprueba intervalos. La interfaz no los expone.

## Simulación de trabajos

iniciar_trabajo almacena tipo, inicio y duración en un diccionario de la habitación. finalizar_trabajos recorre la lista de habitaciones y compara el plazo con el tiempo actual: O(h), siendo h la cantidad de habitaciones. Python controla la terminación y registra el evento; React solo muestra el contador. El plazo se conserva en JSON y los errores de guardado restauran el estado anterior. No se agrega un árbol o heap para una lista pequeña de trabajos independientes.
