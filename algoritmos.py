"""Merge Sort estable, implementado por el equipo en Python."""

def mezclar(izquierda, derecha, clave):
    L = []
    i = 0
    j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i][clave] <= derecha[j][clave]:
            L.append(izquierda[i])
            i = i + 1
        else:
            L.append(derecha[j])
            j = j + 1
    while i < len(izquierda):
        L.append(izquierda[i])
        i = i + 1
    while j < len(derecha):
        L.append(derecha[j])
        j = j + 1
    return L

def merge_sort(datos, clave):
    if len(datos) <= 1:
        return datos.copy()
    mitad = len(datos) // 2
    izquierda = merge_sort(datos[:mitad], clave)
    derecha = merge_sort(datos[mitad:], clave)
    return mezclar(izquierda, derecha, clave)
