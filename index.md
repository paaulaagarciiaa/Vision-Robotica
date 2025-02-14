---
layout: default
title: Mi Blog
---

<div style="display: flex; align-items: center;">
    <img src="/logorobotica.png" alt="Visión Robótica" width="100" height="100" style="margin-right: 20px;">
    <h1>¡Bienvenido a mi blog de Visión Robótica!</h1>
</div>

## Últimos posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
