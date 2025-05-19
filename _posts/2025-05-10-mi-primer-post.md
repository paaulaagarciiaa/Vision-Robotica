---
title: "DÍA 1"
date: 2025-05-10
categories: blog
tags: [practica3]
---

El objetivo de esta práctica es conseguir que el robot sea capaz de estimar su posición y orientación (pose) en un entorno 2D utilizando balizas visuales, concretamente marcadores AprilTag. Para ello, se combinan técnicas de visión por computador con cálculos geométricos, y se emplea la función cv2.solvePnP() para obtener la transformación entre la cámara y el marcador.

Lo primero que hice fue visualizar las imágenes que recibe la cámara del robot mediante HAL.getImage(), y a partir de ahí convertirlas a escala de grises con cv2.cvtColor para facilitar la detección de las etiquetas. Utilicé el detector de AprilTags (pyapriltags.Detector) para localizar los marcadores en la imagen, y dibujé sus esquinas con líneas verdes y su centro con un círculo rojo (ver Figura 1).

<img src="{{ '/imagenes/apriltag.png' | relative_url }}" alt="apriltag" width="900">
<p><em>Figura 1: Visualización de un AprilTag detectado en la imagen.</em></p>

También definí la matriz de calibración intrínseca de la cámara a partir del tamaño de la imagen. Esta matriz es esencial para poder aplicar solvePnP, ya que relaciona las coordenadas 3D del mundo con los píxeles de la imagen. Asumimos que la cámara no tiene distorsión, por lo que los coeficientes de distorsión se fijaron a cero.

Una vez detectados los tags, extraje su ID y consulté su posición real en el entorno a través de un archivo YAML proporcionado, que define las coordenadas conocidas de cada marcador. Esto permite mostrar la posición exacta del tag en el mundo y saber si el sistema lo está detectando correctamente.
