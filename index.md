---
layout: default
title: Mi Blog
---

# ¡Bienvenido a mi blog de Visión Robótica!

## Últimos posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
