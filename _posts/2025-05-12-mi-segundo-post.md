---
title: "DÍA 2"
date: 2025-05-12
categories: blog
tags: [practica3]
---

En esta segunda fase de la práctica, se implementa un sistema de localización visual capaz de estimar correctamente la posición inicial del robot sin movimiento. 

Una vez detectado un marcador en la imagen mediante el detector de pyapriltags, se aplican técnicas para estimar la transformación entre el sistema de coordenadas del tag y la cámara. Para ello, se emplea cv2.solvePnP, que permite obtener:

- rvec: vector de rotación.

- tvec: vector de traslación.

Ambos parámetros definen la transformación T<sub>cam_tag</sub>, que se invierte para obtener T<sub>tag_cam</sub>, es decir, la posición de la cámara respecto al marcador.

A continuación, se concatenan las siguientes matrices de transformación homogénea para estimar la pose del robot en el mundo:

1. T<sub>world_tag</sub>: posición conocida del marcador en el mundo (extraída del YAML).

2. T<sub>tag_optical</sub>: conversión del sistema de coordenadas del marcador (estilo AprilTag, con X hacia delante, Y a la izquierda y Z hacia arriba) al sistema óptico de OpenCV (X hacia la derecha, Y hacia abajo, Z hacia delante). Esta rotación adapta la referencia de coordenadas a la convención del sistema de visión.
   
3. T<sub>tag_cam</sub>: resultado de invertir la transformación que se obtiene con solvePnP (posición de la cámara respecto a la etiqueta).

4. T<sub>optical_camera</sub>: en este caso es la identidad, ya que se considera que el marco óptico y el de la cámara coinciden.

5. T<sub>camera_robot</sub>: posición de la cámara respecto al robot (obtenida del modelo SDF).

La composición completa:

<div align="center"><strong>T<sub>world_robot</sub> = T<sub>world_tag</sub> · T<sub>tag_optical</sub> · T<sub>tag_cam</sub> · T<sub>optical_camera</sub> · T<sub>camera_robot</sub></strong></div>

Desde esta matriz se extrae la posición (x, y) del robot y la orientación yaw, calculada como:

yaw = atan2(rot[1, 0], rot[0, 0]) + π/2

Este ajuste compensa la orientación del eje frontal del robot respecto al marco del mundo.

Se puede ver el resultado de la autolocalización en la Figura 1.

<img src="{{ '/imagenes/autolocalizacion2.png' | relative_url }}" alt="autolocalizacion.png" width="600">
<p><em>Figura 1: Visualización de la autolocalización del robot.</em></p>
