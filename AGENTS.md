# Agents Guide

## Project Overview

Personal website for Eric Daoud Attoyan, built with [Astro](https://astro.build/). Static site deployed to https://edaoud.com.

## Repository Structure

```
src/
  content.config.ts      # Content collection schemas (blog)
  content/blog/           # Blog posts as Markdown files
  layouts/Base.astro      # Shared layout (header, footer, theme toggle)
  pages/
    index.astro           # Homepage
    music.astro           # Music page
    photography.astro     # Photography page
    blog/
      index.astro         # Blog listing with tag filters
      [...slug].astro     # Individual blog post template
      tags/[tag].astro    # Posts filtered by tag
public/
  blog/<post-name>/       # Blog post images, organized by post
  photos/                 # Photography images
```

## Writing a Blog Post

1. Create a new Markdown file at `src/content/blog/<slug>.md`
2. Add the required frontmatter:

```md
---
title: "Post Title"
date: YYYY-MM-DD
description: "Optional short description."
tags: ["tag1", "tag2"]
---

Post content here...
```

3. For images, put them in `public/blog/<slug>/` and reference with:

```md
![Alt text](/blog/<slug>/image.jpg)
```

## Frontmatter Schema

| Field         | Type       | Required | Default |
|---------------|------------|----------|---------|
| `title`       | string     | yes      |         |
| `date`        | date       | yes      |         |
| `description` | string     | no       |         |
| `tags`        | string[]   | no       | `[]`    |

## Commands

- `npm run dev` — Start dev server
- `npm run build` — Build for production
- `npm run preview` — Preview production build

## Style Guidelines

- The site uses a monospace font, minimal design, and supports light/dark themes.
- Keep blog posts concise and focused.
- Use plain Markdown (not MDX). No external component dependencies.
- Images are served from `public/` as-is (no image optimization pipeline).
