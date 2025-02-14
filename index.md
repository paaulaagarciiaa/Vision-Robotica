---
layout: default
title: Mi Blog
---

<div style="display: flex; align-items: center;">
    <img src="/logorobotica.png" alt="Visión Robótica" width="50" height="50" style="margin-right: 10px;">
    <h1 style="margin: 0;">Visión Robótica</h1>
</div>

## ¡Bienvenido a mi blog de Visión Robótica!

<div style="display: flex; align-items: center;">
    <img src="/logorobotica.png" alt="Visión Robótica" width="40" height="40" style="margin-right: 20px;">
    <h1 style="margin: 0;">Explorando la visión artificial y la robótica</h1>
</div>

## Últimos posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
