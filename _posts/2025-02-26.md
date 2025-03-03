---
title: "DÍA 2"
date: 2025-02-26
categories: blog
---

Después de conseguir que el coche siguiera la línea roja en el circuito, el siguiente problema era hacerlo más eficiente. Primero me aseguré de que pudiera completar el recorrido sin fallos y luego intenté reducir el tiempo de vuelta. 

Uno de los principales cambios ha sido añadir un segundo controlador PID para la velocidad. Antes, la velocidad del coche era constante, lo que dificultaba los giros en curvas cerradas. Ahora, la velocidad se ajusta dinámicamente según el error:
- En rectas, el coche acelera hasta su velocidad máxima.
- En curvas, la velocidad se reduce dependiendo de la magnitud del error, evitando que el coche se salga.













