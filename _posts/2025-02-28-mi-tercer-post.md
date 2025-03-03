---
title: "DÍA 3"
date: 2025-02-28
categories: blog
---

Mi objetivo era que el coche fuese más rápido y estable sin perder precisión en las curvas. Hasta ahora, el coche conseguía completar el circuito sin problemas, pero todavía tardaba demasiado y oscilaba en giros cerrados. Para mejorar esto, hice varios cambios en la velocidad, el control de giro y el cálculo del error.

Uno de los cambios más importantes fue incrementar la velocidad máxima en rectas a 27.0, mucho mayor que en versiones anteriores. Sin embargo, con esta velocidad, el coche se salía en curvas cerradas, así que añadí un sistema de frenado adaptativo:
- Si el error es grande (curva fuerte), la velocidad baja a 4.5.
- En curvas menos cerradas, la velocidad se ajusta dinámicamente entre 4.0 y 27.0 según la magnitud del error.

El PID que había usado para la velocidad decido eliminarlo porque no veía que me funcionase. En su lugar, la velocidad se reduce directamente en función del error. Esto hace que el coche acelere en rectas y frene solo cuando es necesario, lo que mejora bastante el tiempo de vuelta.

Hasta ahora, el error se calculaba ponderando en 85% la posición del punto adelantado y 15% el centroide de la línea. Esto hacía que el coche reaccionara un poco tarde en algunas curvas. En esta versión, ajusté la ponderación a 95% en el punto adelantado y 5% en el centroide.

Para entender mejor qué está detectando el coche y cómo está tomando decisiones, añadí una mejora visual en el código. Ahora el programa dibuja el contorno de la línea roja detectada, un punto verde en el punto adelantado, que es el que usa el coche para calcular el error y una línea verde desde el centro de la imagen hasta el punto detectado, permitiendo ver en tiempo real si el coche está siguiendo bien la trayectoria (ver Figura 1).

<img src="{{ '/imagenes/dia3.png' | relative_url }}" alt="Nueva visualización" width="600">
<p><em>Figura 1: Visualización de contornos, líneas y punto verde para depuración.</em></p>

El coche holonómico ahora completa el circuito en 40 segundos, muchísimo más rápido que en versiones anteriores. Aunque sigue habiendo algo de oscilación en las curvas, el rendimiento ha mejorado bastante y el coche es mucho más eficiente en la pista (ver Figura 2).

<iframe width="560" height="315" src="https://www.youtube.com/embed/XcsPPe5625A" frameborder="0" allowfullscreen></iframe>
<p><em>Figura 2: Visualización coche holonómico recorriendo el circuito simple en 40 segundos.</em></p>



