---
title: "DÍA 2"
date: 2025-04-07
categories: blog
tags: [practica2]
---


En esta segunda versión, el objetivo ha sido encontrar el punto homólogo en la imagen derecha a partir de un punto conocido en la imagen izquierda. Este paso es clave para poder hacer más adelante la triangulación.

Lo primero que hice fue generar la línea epipolar correspondiente a un punto de la imagen izquierda. Para ello, utilicé la función HAL.graficToOptical() para convertir ese punto, dado en coordenadas gráficas (pixeles), al sistema óptico de la cámara. Luego, con HAL.backproject(), obtuve el rayo 3D que parte desde la posición de la cámara izquierda y pasa por ese punto en el espacio. Con este rayo definido, muestreo 300 puntos a lo largo de él variando el parámetro λ, y proyecto todos esos puntos sobre la imagen derecha usando HAL.project(). El resultado es una nube de puntos que, vista desde la cámara derecha, se alinean formando una línea epipolar. Esta línea representa las posibles ubicaciones del punto homólogo en la imagen derecha, y constituye la restricción epipolar asociada al punto izquierdo.

Ahora bien, no me interesan todos esos puntos, sino únicamente aquellos que caen sobre los bordes detectados en la imagen derecha. Esos serán mis candidatos (puntos verdes pintados sobre la línea epipolar pintados sobre la Figura 1). Para cada uno de ellos, comparo un parche de 11x11 píxeles centrado en el punto candidato con el parche del mismo tamaño en la imagen izquierda, y uso como métrica el error cuadrático medio. El que tenga menor diferencia será el punto homólogo (punto azul pintado sobre la Figura 1).

<img src="{{ '/imagenes/candidatos.png' | relative_url }}" alt="candidatos" width="600">
<p><em>Figura 1: Línea epipolar y puntos candidatos sobre bordes en la imagen derecha.</em></p>

Una vez encontrado el matching, lo visualizo marcando el punto izquierdo en verde, el derecho en azul, y dibujo una línea amarilla entre ellos con cv2.line para representar la correspondencia encontrada (ver Figura 2).

<img src="{{ '/imagenes/matching.png' | relative_url }}" alt="matching" width="600">
<p><em>Figura 2: Matching visual entre puntos homólogos con línea de conexión.</em></p>


Además, para empezar a conectar esto con la reconstrucción en 3D, hice una pequeña prueba de retroproyectar un punto cualquiera sobre el rayo (sin triangulación aún), y lo pinté directamente en el visor 3D. Esta prueba fue útil para comprobar que todo está bien alineado y que el rayo está bien calculado.







