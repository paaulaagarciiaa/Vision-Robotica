---
layout: default
title: Mi Blog
---

<table>
  <tr>
    <td>
      <img src="https://paaulaagarciiaa.github.io/Vision-Robotica/logorobotica.png" alt="Visión Robótica" width="50" height="50">
    </td>
    <td>
      <h1 style="margin: 0; font-size: 26px;">¡Bienvenido a mi blog de Visión Robótica!</h1>
      <p><strong>Por {{ site.author }}</strong></p>  <!-- Aquí se muestra el autor -->
    </td>
  </tr>
</table>

## PRÁCTICA 1: Visual Follow Line

<details style="margin-bottom: 30px;">
<summary><strong>Ver entradas P1</strong></summary>
<img src="{{ '/f1.png' | relative_url }}" alt="Imagen de la práctica 1" style="width: 200px; height: auto;">



<ul>
{% for post in site.posts reversed %}
  {% if post.tags contains "practica1" %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>

</details>


## PRÁCTICA 2: 3D Reconstruction

<details style="margin-bottom: 30px;">
<summary><strong>Ver entradas P2</strong></summary>
<img src="{{ '/3d_reconstruction.png' | relative_url }}" alt="Imagen de la práctica 2" style="width: 200px; height: auto;">



<ul>
{% for post in site.posts reversed %}
  {% if post.tags contains "practica2" %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>

</details>


## PRÁCTICA 3: Marker Visual Localization

<details>
<summary><strong>Ver entradas P3</strong></summary>
<img src="{{ 'imagenes/p3.png' | relative_url }}" alt="Imagen de la práctica 3" style="width: 200px; height: auto;">



<ul>
{% for post in site.posts reversed %}
  {% if post.tags contains "practica3" %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>

</details>


