import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Uso defaultdict(int) para que arranque automáticamente en 0.
ventas_por_fecha = defaultdict(int)

# Diccionario para contar cuántas unidades se vendieron de cada producto.
ventas_productos = defaultdict(int)

ventas_totales = 0

ventas_del_mes = 0

# Abrimos el archivo CSV en modo lectura.
with open("datos/datos.csv", "r", encoding="utf-8") as archivo:

    # Creamos el lector CSV usando ";" como separador.
    lector = csv.reader(archivo, delimiter=";")

    # Saltamos la fila de encabezados.
    next(lector)

    # Recorremos cada fila del archivo.
    for fila in lector:

        # Guardamos los datos de cada columna en variables.
        nombre = fila[0]
        cantidad = int(fila[1])
        precio_unitario = int(fila[2])
        fecha = fila[3]

        # Calculamos el total vendido en esa fila.
        venta_total = cantidad * precio_unitario

        # Sumamos al total general de ventas.
        ventas_totales += venta_total

        # Si la fecha pertenece a mayo de 2026,
        # acumulamos las ventas de ese mes.
        if '2026-05' in fecha:     #El filtro del mes está hardcodeado como '2026-05', si el CSV tuviera datos de otro año o se quisiera reutilizar el script habría que cambiarlo a mano. Se podría mejorar usando fecha_dt.month == 5 después de convertir a datetime, así es más flexible. Igual para el TP funciona perfecto, aprobado.
            ventas_del_mes += venta_total

        # Sumamos la cantidad vendida del producto.
        ventas_productos[nombre] += cantidad

        # Convertimos la fecha de texto a datetime
        # para poder ordenarla correctamente después.
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")

        # Acumulamos las ventas por fecha.
        ventas_por_fecha[fecha_dt] += venta_total

# Buscamos el producto con mayor cantidad vendida.
producto_mas_vendido = max(ventas_productos, key=ventas_productos.get) # Se podría haber calculado el producto más vendido dentro del loop para ir actualizándolo fila por fila, pero hacerlo al final después de procesar todo el CSV es más eficiente porque evita llamar a max() en cada iteración. Buena decisión.



# Mostramos resultados por pantalla.
print(f'Producto más vendido: {producto_mas_vendido}')
print(f'Ventas totales: ${ventas_totales:,}')
print(f'Ventas del mes (mayo): ${ventas_del_mes:,}')


# Ordenamos las fechas para que el gráfico salga correctamente.
fechas_ordenadas = sorted(ventas_por_fecha.keys())

# Generamos una lista con las ventas correspondientes a cada fecha.
ventas_ordenadas = [ventas_por_fecha[f] for f in fechas_ordenadas]

# Definimos el tamaño de la figura.
plt.figure(figsize=(14, 5))

# Creamos el gráfico de líneas.
plt.plot(
    fechas_ordenadas,
    ventas_ordenadas,
    marker='o',
    color='steelblue',
    linewidth=2
)

# Título del gráfico.
plt.title("Evolución de Ventas Diarias")

# Nombre del eje X.
plt.xlabel("Fecha")

# Nombre del eje Y.
plt.ylabel("Ventas ($)")

# Rotamos las fechas para que se lean mejor.
plt.xticks(rotation=45, ha='right')

# Ajusta automáticamente los márgenes.
plt.tight_layout()

# Guardamos el gráfico como imagen PNG.
plt.savefig("resultados/grafico_ventas.png")

# Mostramos el gráfico en pantalla.
plt.show()
