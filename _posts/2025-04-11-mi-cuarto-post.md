---
title: "DÍA 4"
date: 2025-04-11
categories: blog
tags: [practica2]
---

En esta última versión, el objetivo ha sido pintar todos los puntos reconstruidos en 3D, pero esta vez asignándoles color en lugar de mostrarlos con un color fijo. Para ello, he tomado el parche de 11×11 píxeles alrededor del punto en la imagen izquierda original (en color), y he calculado la media del color para cada parche. Ese color medio se ha asociado a su punto 3D correspondiente, permitiendo así una visualización más realista en el visor.

Además, he añadido un filtro bilateral antes de aplicar Canny, con el fin de eliminar detalles pequeños o ruido de las imágenes sin perder bordes importantes. 

Por motivos de rendimiento y visualización, no he procesado todos los puntos detectados. En total, el filtro de Canny detectó aproximadamente 16.000 puntos en la imagen izquierda, pero decidí aleatorizarlos con np.random.shuffle(pointsL) y quedarme solo con 10.000 de ellos para la reconstrucción final. Esto permite mantener un equilibrio entre densidad de puntos y fluidez en la ejecución.
El resultado final permite distinguir la silueta de los personajes principales (como Mario, Bowser o Toad), aunque todavía se aprecian algunos puntos que no reconstruyen nada y generan algo de ruido visual. Aun así, se consigue una representación general fiel de la escena, lo que demuestra que el sistema de reconstrucción está funcionando correctamente.

En la Figura 1 se puede ver el resultado final de la práctica 2.

### Resultado final P2 3D Reconstruction
<iframe width="560" height="315" src="https://www.youtube.com/embed/_n2owitwYAY" frameborder="0" allowfullscreen></iframe>
<p><em>Figura 1: Visualización final reconstrucción 3D.</em></p>




