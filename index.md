---
layout: default
title: Mi Blog
---

<div style="display: flex; align-items: center; gap: 15px;">
    <img src="/logorobotica.png" alt="Visión Robótica" width="50" height="50">
    <span style="font-size: 26px; font-weight: bold;">¡Bienvenido a mi blog de Visión Robótica!</span>
</div>

## Últimos posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
