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
    </td>
  </tr>
</table>

## PRÁCTICA 1: Visual Follow Line
<img src="{{ '/f1.png' | relative_url }}" alt="Imagen de la práctica 1" style="width: 300px; height: auto;">

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
