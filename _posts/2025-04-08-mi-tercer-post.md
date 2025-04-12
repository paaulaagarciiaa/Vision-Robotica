---
title: "DÍA 3"
date: 2025-04-08
categories: blog
tags: [practica2]
---

Una vez establecido el punto homólogo en la imagen derecha, comencé con el proceso de triangulación, trabajando inicialmente con un único punto para asegurarme de que el procedimiento era correcto antes de aplicarlo al conjunto de puntos.

Para ello, primero convertí el punto de la imagen derecha a coordenadas gráficas y luego a coordenadas ópticas utilizando HAL.graficToOptical(). A partir de ese punto óptico, y mediante la función HAL.backproject(), obtuve el rayo 3D que conecta el centro óptico de la cámara derecha con la escena. Realicé el mismo procedimiento con el punto de la cámara izquierda, de manera que obtuve dos rayos en el espacio tridimensional, cada uno con su vector director.

Ambos vectores se normalizaron y se planteó un sistema lineal con tres ecuaciones y dos incógnitas (uno para cada parámetro escalar λ). Este sistema se resolvió mediante mínimos cuadrados con np.linalg.lstsq, obteniendo así los valores de 𝜆L y 𝜆R que permiten determinar los puntos más cercanos entre los dos rayos. El punto triangulado final se calcula a partir del rayo izquierdo y su parámetro correspondiente (resumen triangulación Figura 1).
<img src="{{ '/imagenes/triangulacion.png' | relative_url }}" alt="triangulacion" width="600">
<p><em>Figura 1: Esquema del proceso de triangulación 3D a partir de correspondencias estéreo.</em></p>


Para facilitar su visualización en el visor 3D, escalé el punto triangulado, ya que sus coordenadas eran muy grandes. Además, representé visualmente los rayos desde ambas cámaras hasta el punto, lo cual me sirvió para verificar que la triangulación era coherente (ver Figura 2).

<img src="{{ '/imagenes/rayos.png' | relative_url }}" alt="rayos" width="600">
<p><em>Figura 2:.</em></p>

Una vez validado el proceso, lo extendí al conjunto completo de puntos de interés, aunque inicialmente todos los puntos se mostraban con el mismo color (negro), y el ruido visual era notable, sin llegar a reconocer la estructura de la reconstrucción 3D (ver Figura 3).

<img src="{{ '/imagenes/puntosnegros.png' | relative_url }}" alt=" puntosnegros " width="600">
<p><em>Figura 3: Representación 3D puntos de color negro.</em></p>


