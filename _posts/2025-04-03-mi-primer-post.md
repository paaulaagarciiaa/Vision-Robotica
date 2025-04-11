---
title: "DÍA 1"
date: 2025-04-03
categories: blog
tags: [practica2]
---


El objetivo de esta práctica es conseguir que el robot Kobuki sea capaz de generar una reconstrucción 3D del entorno utilizando la información que captan sus dos cámaras, una a la izquierda y otra a la derecha. Para ello, tenemos que implementar paso a paso toda la lógica necesaria para extraer información 3D a partir de las imágenes 2D, usando conceptos como la retroproyección, la triangulación y la búsqueda de correspondencias.

Empecé visualizando las imágenes que capturan las dos cámaras. Para esto utilicé la función HAL.getImage() para obtener las imágenes en bruto, y GUI.showImages() para mostrarlas, como se puede ver en la Figura 1. También obtuve la posición de ambas cámaras en el espacio 3D con HAL.getCameraPosition(), lo cual es clave porque más adelante necesitaremos esas posiciones para calcular las direcciones de los rayos y hacer la triangulación.

<img src="{{ '/imagenes/escena.png' | relative_url }}" alt="escena" width="600">
<p><em>Figura 1: Visualización cámara izquierda y derecha.</em></p>

Después, hice un pequeño preprocesado de las imágenes convirtiéndolas a escala de grises y aplicando el filtro de Canny (ver Figura 2) para detectar los bordes. Esto me permitió generar una primera lista de puntos de interés en la imagen izquierda. Antes de usar todos, para ir probando el sistema poco a poco, selecciono un único punto de prueba de la imagen izquierda y sobre ese construyo un primer rayo 3D.

<img src="{{ '/imagenes/canny.png' | relative_url }}" alt="canny" width="600">
<p><em>Figura 2: Detector de bordes Canny.</em></p>

Para construir ese rayo, convertí las coordenadas gráficas del punto al sistema óptico con HAL.graficToOptical() y a partir de ahí, usando HAL.backproject(), obtuve la dirección en la que se proyecta el rayo desde la cámara izquierda hacia el espacio. Como todavía no tengo implementada la triangulación ni el emparejamiento con la imagen derecha, simplemente pinté ese punto en verde en la imagen izquierda para asegurarme de que todo funcionaba bien.




