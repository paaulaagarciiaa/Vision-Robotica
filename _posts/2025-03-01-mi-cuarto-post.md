---
title: "DÍA 4"
date: 2025-03-01
categories: blog
---

Una vez conseguí que el coche completara el circuito en 40 segundos, cambié al circuito simple con el coche Ackermann, este no puede girar sobre su eje, necesita moverse para cambiar de dirección y su capacidad de giro está limitada por su radio de giro. Esto lo hace más estable en curvas, pero menos ágil en rectas.

Debido a estas diferencias, el PID que funcionaba en el otro coche no se comporta igual aquí. En rectas, el coche oscila demasiado. Además, el PID sobrecorrige los pequeños errores, lo que hace que el coche se vuelva inestable a altas velocidades.

Para evitar las oscilaciones en rectas, probé a introducir una banda muerta, es decir, que el coche ignore pequeños errores en la detección de la línea. Esto ayudó a reducir un poco las vibraciones, pero el coche sigue siendo muy nervioso y, en ocasiones, acaba chocando o incluso girando en el sentido contrario.

También probé a suavizar la transición entre giros con un factor de suavizado (SMOOTHING_FACTOR = 0.5), que evita cambios bruscos en la dirección. Esto ha mejorado un poco la estabilidad, pero el coche todavía se vuelve incontrolable en ciertas rectas.

Un problema grave que apareció en esta versión es que el coche a veces se gira demasiado y empieza a ir en sentido contrario. Esto ocurre cuando:
- Pierde la línea y toma una dirección incorrecta.
- El PID hace una corrección excesiva y el coche gira más de la cuenta.
- En algunas situaciones, el coche rebota contra un obstáculo y cambia completamente de dirección.
En estos casos, el coche deja de seguir la trayectoria correcta y empieza a moverse en sentido opuesto, lo que hace que se vuelva incontrolable y acabe chocando.

Por ahora, el coche no es capaz de completar la vuelta entera con este código. Sigue siendo demasiado inestable en rectas y no corrige bien cuando pierde la trayectoria (ver Figura 1).

<iframe width="560" height="315" src="https://www.youtube.com/embed/aOyMU9rRIx8" frameborder="0" allowfullscreen></iframe>
<p><em>Figura 1: Visualización del coche Ackermann recorriendo el circuito simple. El coche acaba chocándose y girando en sentido contrario.</em></p>



