---
title: "DÍA 1"
date: 2025-02-25
categories: blog
---

Para esta práctica, el coche de Fórmula 1 debe recorrer un circuito siguiendo una línea roja. Al principio, me centré en entender el problema y en cómo hacer que el coche pudiera detectar y seguir la línea correctamente.

El primer paso fue procesar la imagen capturada por la cámara del coche. Para ello, convertí la imagen de BGR a HSV, lo que facilita la identificación de la línea roja. Usé dos rangos de color en HSV para detectar los tonos rojos, combinando ambas máscaras binarias en una única imagen. Para reducir el ruido y evitar detecciones erróneas, recorté la parte superior e inferior de la imagen, manteniendo solo la región más relevante donde se encuentra la línea roja en la pista (ver Figura 1).

<img src="{{ '/imagenes/mask.png' | relative_url }}" alt="Máscara detección línea roja" width="600">
<p><em>Figura 1: Máscara detección línea roja.</em></p>

Una vez obtenida la máscara con la línea roja, calculé el error de posición, que es la diferencia entre la posición del centroide de la línea y el centro de la imagen. Este error es fundamental para determinar cuánto debe girar el coche para mantenerse sobre la trayectoria.

Para corregir la dirección del coche, implementé un controlador PID, que ajusta el giro en función del error detectado. Al principio, configuré la velocidad angular con un límite de [−1.5,1.5] para evitar giros bruscos e inestabilidad. Sin este límite, el coche podría girar demasiado rápido y perder el control, provocando movimientos bruscos o incluso saliéndose de la pista. Así consigo que la corrección sea más suave y estable.

Para ajustar el PID, seguí un método de prueba y error. Primero, puse Ki y Kd en cero y ajusté Kp hasta que el coche empezó a oscilar. Una vez que vi que el sistema reaccionaba, aumenté Ki para reducir esas oscilaciones y hacer que el coche se mantuviera mejor en la línea. Finalmente, ajusté Kd para suavizar los giros y evitar que el coche reaccionara de forma demasiado brusca.

Inicialmente, configuré el coche con una velocidad constante, lo que permite evaluar cómo responde el control sin introducir más variables. En rectas, el coche se mantiene estable sobre la línea, pero en la primera curva se desvía demasiado y termina chocando contra la pared. Esto indica que todavía necesito hacer ajustes, sobre todo en curvas cerradas, para mejorar la estabilidad y que el coche no se salga de la pista.





