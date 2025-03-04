---
title: "DÍA 6"
date: 2025-03-03
categories: blog
---

Mi último objetivo era reducir el tiempo que tarda el coche Ackermann en completar el circuito simple, ya que en la versión del día anterior conseguía dar la vuelta, pero en 3 minutos, un tiempo demasiado alto. He probado diferentes ajustes en los parámetros para hacerlo más rápido, pero al subir la velocidad o modificar el PID, el coche empezaba a oscilar demasiado y acababa chocándose.

Después de varios intentos, la versión del DÍA 5 sigue siendo la que mejor funciona, ya que mantiene el coche estable y consigue completar el circuito sin problemas, aunque sigue siendo lento.

También he probado el coche en distintos circuitos y, aunque consigue terminarlos todos, el tiempo sigue siendo muy alto. El principal problema es que en línea recta va demasiado lento, ya que los ajustes que evitan que oscile también limitan su velocidad en tramos largos sin curvas. Esto hace que, aunque sea estable, no consiga mejorar tiempos de vuelta, obteniendo un resultado de 450 segundos en el circuito de Nurburgring (ver Figura 1), 375 segundos en el circuito Montmelo (ver Figura 2), y 850 segundos en el circuito de Montreal (ver Figura 3).

### Circuito Nurburgring
<iframe width="560" height="315" src="https://www.youtube.com/embed/tGNvfuC6fDc" frameborder="0" allowfullscreen></iframe>
<p><em>Figura 1: Visualización del coche Ackermann recorriendo el circuito Nurburgring en 450 segundos (velocidad x8).</em></p>

### Circuito Montmelo
<iframe width="560" height="315" src="https://www.youtube.com/embed/CL5jhTi4Vpw" frameborder="0" allowfullscreen></iframe>
<p><em>Figura 2: Visualización del coche Ackermann recorriendo el circuito Montmelo en 375 segundos (velocidad x8).</em></p>

### Circuito Montreal
<iframe width="560" height="315" src="https://www.youtube.com/embed/hB8LpoofkKI" frameborder="0" allowfullscreen></iframe>
<p><em>Figura 3: Visualización del coche Ackermann recorriendo el circuito Montreal en 850 segundos (velocidad x8).</em></p>
