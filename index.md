---
layout: default
title: Mi Blog
header:
  overlay_image: "/logorobotica.png"
---

# ¡Bienvenido a mi blog de Visión Robótica!

## Últimos posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
