---
layout: page
title: Photography
permalink: /photography/
cover: camera.jpg
last_modified_at: 2020-05-12
image: /assets/img/eric.jpg
---

<p class="mb-5">
  I have been keen on photography since 2010.
  I mostly take landscape pictures and I am trying to get into street
  photography.

  I uploaded all my pictures on my
  <a href="https://500px.com/p/ericda?view=photos">500px gallery</a>.
  Here are some of my favorite shots.
</p>

{%- for picture in site.data.pictures -%}
  <div class='pixels-photo'>
    <p>
      <img src='{{ picture.url }}' alt='{{ picture.title }}'>
    </p>
  </div>

  <p class="font-weight-bold mb-5">
    {{ picture.title }}. {{ picture.location }} ({{ picture.year}})
  </p>
{%- endfor -%}
