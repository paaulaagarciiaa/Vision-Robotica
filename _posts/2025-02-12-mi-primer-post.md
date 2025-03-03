---
title: "DÍA 1"
date: 2025-02-25
categories: blog
---

Para esta práctica, el coche de Fórmula 1 debe recorrer un circuito siguiendo una línea roja. Al principio, me centré en entender el problema y en cómo hacer que el coche pudiera detectar y seguir la línea correctamente.

Lo primero fue procesar la imagen que captura la cámara del coche. Convertí la imagen a HSV para filtrar los tonos rojos y así detectar la línea, también recorté la imagen para eliminar ruido y evitar que el coche detecte elementos irrelevantes del entorno. 

<img src="https://paaulaagarciiaa.github.io/Vision-Robotica/_posts/mask.png" alt="Máscara detección línea roja" width="100">



