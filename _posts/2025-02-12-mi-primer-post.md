---
title: "DÍA 1"
date: 2025-02-25
categories: blog
---

Para esta práctica, el coche de Fórmula 1 debe recorrer un circuito siguiendo una línea roja. Al principio, me centré en entender el problema y en cómo hacer que el coche pudiera detectar y seguir la línea correctamente.

Lo primero fue procesar la imagen que captura la cámara del coche. Convertí la imagen a HSV para filtrar los tonos rojos y así detectar la línea, también recorté la imagen para eliminar ruido y evitar que el coche detecte elementos irrelevantes del entorno. 

<img src="{{ '/imagenes/mask.png' | relative_url }}" alt="Máscara detección línea roja" width="600">
<p><em>Figura 1: Máscara detección línea roja.</em></p>

Una vez obtenida la línea roja, calculé el error entre el centro de la imagen y el centroide de la línea, lo que indica cuánto debe girar el coche para mantenerse sobre ella. Para corregir la dirección, implementé un controlador PID que ajusta el giro en función del error.

Inicialmente, configuré el coche con una velocidad constante, lo que permite ver cómo responde el control sin introducir más variables. En rectas se mantiene estable, pero en la primera curva se desvía demasiado y termina chocando contra la pared. Esto indica que el sistema no está reaccionando bien en giros cerrados.




