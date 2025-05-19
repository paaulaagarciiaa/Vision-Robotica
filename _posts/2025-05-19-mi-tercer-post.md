---
title: "DÍA 3"
date: 2025-05-19
categories: blog
tags: [practica3]
---

Una vez comprobado que el robot es capaz de localizarse correctamente al inicio gracias a las balizas visuales, el siguiente paso fue introducir movimiento. Para empezar, simplemente se añadió velocidad lineal, y el robot avanzaba mostrando su posición estimada en rojo.

El problema vino cuando el robot dejaba de ver balizas. En ese momento, la estimación se quedaba congelada porque no tenía nueva información. Para solucionarlo, se decidió incluir la odometría como apoyo: si no se detecta ninguna etiqueta, se calcula el desplazamiento usando los valores de odometría y se actualiza la posición a partir de la última estimación conocida.

El sistema se comporta entonces de la siguiente forma:

- Si se ve alguna baliza, se calcula la posición con visión, usando la composición de transformaciones:
 T<sub>world_robot</sub> = T<sub>world_tag</sub> · T<sub>tag_optical</sub> · T<sub>tag_cam</sub> · T<sub>camera_robot</sub>
 Esto da directamente la pose del robot en el mundo.
- Si no se ve ninguna baliza, se usa el incremento de odometría para actualizar la última pose calculada. Básicamente, se suma el desplazamiento local (dx, dy, dyaw) a la posición anterior, teniendo en cuenta el ángulo para hacerlo en coordenadas globales.

Con este sistema, el robot puede seguir actualizando su posición estimada aunque momentáneamente no vea ninguna etiqueta, lo que evita que se quede "parado" desde el punto de vista de la estimación. Esto se puede ver en la simulación, donde el robot rojo sigue moviéndose y actualizando su trayectoria incluso cuando no hay detecciones visuales (ver Figura 1).

### Resultado final Práctica 3 Marker Based Visual Loc
