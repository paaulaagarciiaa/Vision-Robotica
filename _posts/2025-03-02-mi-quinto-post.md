---
title: "DÍA 5"
date: 2025-03-02
categories: blog
tags: [practica1]
---

En esta versión he conseguido que finalmente pueda dar la vuelta entera, sin embargo, aunque ya no se choca ni gira en sentido contrario, tarda 3 minutos en completar el recorrido, lo que sigue siendo demasiado lento (ver Figura 1).

Uno de los cambios más importantes fue ajustar la velocidad para que el coche fuera más estable sin perder rapidez. Ahora adapta mejor su velocidad en curvas y evita cambios bruscos, pero sigue perdiendo demasiado tiempo en líneas rectas. Probé a subir la velocidad máxima, pero si la aumento demasiado, el coche empieza a oscilar y acaba chocándose.

Hasta ahora, el cálculo del error ponderaba en 95% el punto adelantado y 5% el centroide, lo que ayudaba a anticipar los giros. En esta versión, aumenté aún más esta anticipación, 99% el punto adelantado y 1% el centroide.

Ahora el PID se ajusta según si el coche está en una curva o en una recta, algo que antes no hacía. Si el error es mayor de 0.25, el control se vuelve más agresivo para corregir más rápido. En curvas cerradas, Kp y Kd aumentan automáticamente para mejorar la reacción, y si el giro es demasiado flojo, se aplica un mínimo de 0.3 para que no tarde en corregir. Esto ha mejorado la estabilidad en curvas.

Para que el coche no haga giros bruscos, aumenté el suavizado del giro a 0.6 (correction_w), así las correcciones son más progresivas. También hice que el límite de giro máximo (W_max) cambie según la situación: en rectas se mantiene igual, pero en curvas aumenta un 30% para que pueda girar mejor sin quedarse corto.

<iframe width="560" height="315" src="https://www.youtube.com/embed/SkMLvX-J-no" frameborder="0" allowfullscreen></iframe>
<p><em>Figura 1: Visualización del coche Ackermann recorriendo el circuito simple en 180 segundos (velocidad x4).</em></p>

