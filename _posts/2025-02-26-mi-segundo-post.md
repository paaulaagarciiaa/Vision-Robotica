---
title: "DÍA 2"
date: 2025-02-26
categories: blog
tags: [practica1]
---

El objetivo de esta versión era que el coche holonómico completase el recorrido sin fallos, intentando también reducir el tiempo de vuelta.

Uno de los principales cambios ha sido añadir un segundo controlador PID para la velocidad. Antes, la velocidad del coche era constante, lo que dificultaba los giros en curvas cerradas. Ahora, la velocidad se ajusta dinámicamente según el error:
- En rectas, el coche acelera hasta su velocidad máxima.
- En curvas, la velocidad se reduce dependiendo de la magnitud del error, evitando que el coche se salga.

También ajusté los parámetros del PID para el giro y fui aumentando la velocidad máxima y mínima, para que el coche reaccione más rápido a los cambios de dirección, y que fuese más rápido. 

Otro cambio importante fue la forma de calcular el error. Antes, el coche solo usaba el centroide de la línea roja, lo que hacía que reaccionara con retraso en las curvas. Ahora, pondera en un 85% la posición del punto más adelantado de la línea y en un 15% el centroide. Esto le permite anticipar curvas y corregir antes la dirección, reduciendo las oscilaciones y haciendo el control más fluido.

Gracias a estos ajustes, el tiempo de vuelta bajó de 10 minutos a 4. Aún tengo que mejorar la precisión en curvas cerradas, ya que el coche sigue oscilando bastante, pero al menos ya completa el circuito mucho más rápido y sin perder la línea.












