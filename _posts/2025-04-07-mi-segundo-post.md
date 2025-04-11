---
title: "DÍA 2"
date: 2025-04-07
categories: blog
tags: [practica2]
---


En esta segunda versión, el objetivo ha sido encontrar el punto homólogo en la imagen derecha a partir de un punto conocido en la imagen izquierda. Este paso es clave para poder hacer más adelante la triangulación.

Lo primero que hice fue construir la línea epipolar. Para ello, tomé el punto izquierdo de referencia y generé un rayo en el espacio usando las funciones HAL.graficToOptical() y HAL.backproject(). A partir de ese rayo, muestreo 300 puntos en el espacio y los proyecto sobre la imagen derecha con HAL.project(). Esto me da una nube de puntos que en la imagen derecha forma una línea, y esa línea es justo la restricción epipolar del punto izquierdo (puntos rojos pintados en la Figura 1).

Ahora bien, no me interesan todos esos puntos, sino únicamente aquellos que caen sobre los bordes detectados en la imagen derecha. Esos serán mis candidatos (puntos verdes pintados sobre la línea epipolar pintados sobre la Figura 1). Para cada uno de ellos, comparo un parche de 11x11 píxeles centrado en el punto candidato con el parche del mismo tamaño en la imagen izquierda, y uso como métrica el error cuadrático medio. El que tenga menor diferencia será el punto homólogo (punto azul pintado sobre la Figura 1).

<img src="{{ '/imagenes/candidatos.png' | relative_url }}" alt="candidatos" width="600">
<p><em>Figura 1: Línea epipolar y puntos candidatos sobre bordes en la imagen derecha.</em></p>

Una vez encontrado el matching, lo visualizo dibujando el punto izquierdo en verde, el derecho en azul y una línea amarilla que los conecta (ver Figura 2). 

<img src="{{ '/imagenes/matching.png' | relative_url }}" alt="matching" width="600">
<p><em>Figura 2: Matching visual entre puntos homólogos con línea de conexión.</em></p>


Además, para empezar a conectar esto con la reconstrucción en 3D, hice una pequeña prueba de retroproyectar un punto cualquiera sobre el rayo (sin triangulación aún), y lo pinté directamente en el visor 3D. Esta prueba fue útil para comprobar que todo está bien alineado y que el rayo está bien calculado.







