---
layout: post
title: Deploy Metabase with Docker and Nginx over HTTPS
date: 2020-05-16
last_modified_at: 2020-05-16
excerpt:
    Metabase is an open source dataviz application that lets you create
    analytics graphs and dashboards very easily. Let's see how to deploy
    Metabase over HTTPS by using Docker, Nginx and
    Let's Encrypt.
cover: metabase.png
image: /assets/img/eric.jpg
categories: ["Software Engineering"]
---

Note: this post won't cover how to use metabase, we just focus on how to
make it work over https with Nginx and Docker.

## Prerequisite

Before we start, you should be familiar with the following tools:

- [Metabase](https://www.metabase.com/) (at least what it's useful for)
- [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)
- [Nginx](https://www.nginx.com/) reverse proxy
- [Let's encrypt](https://letsencrypt.org/) and [Certbot](https://certbot.eff.org/)

You should have `Docker`, `docker-compose` and `Nginx` installed before
we can go on.

I am also going to assume you already have a domain name ready to redirect to
your metabase application and a server to host the app.

## Overview

Here's an overview of the environment we will setup:

- `domain.com/metabase`: Assuming your domain name is `domain.com`, we will
  serve the application under the url `domain.com/metabase`.
- Metabase container: We will use the official
  [Metabase Docker Image](https://www.metabase.com/start/docker), the
  application will run on `localhost:3000`.
- Nginx reverse proxy: Since the application runs on `localhost:3000`, it
  is not accessible to the public yet. With nginx, we will redirect the traffic
  from `domain.com/metabase` to `localhost:3000`.
- Metabase db: Metabase needs to store its metadata in a dedicated database.
  This database could be postgresql or a simple `.h2` file, we use the later
  for more simplicity.
- sqlite.db: This will our main database, the one that contains the data
  we want to visualize with metabase. Note that Metabase is compatible
  with many databases like Postgres, MySQL, Mongo DB, sqlite, etc ...

Let's recap everything on a schema:

<img src="/assets/img/articles/metabase/overview.png" width="60%">

## Setup Metabase container

We use [docker-compose](https://docs.docker.com/compose/) for setting up
the container, here's the `docker-compose.yml` configuration file:

``` yml
version: "3.1"

services:
  metabase:
    image: metabase/metabase:latest  # Use official metabase image, latest version
    volumes:
      - ./.volumes/metabase:/metabase-data  # Metabase container data is stored in .volumes folder
      - ./db.sqlite:/db.sqlite  # This is the main database
    ports:
      - 3000:3000  # Makes metabase accessible on localhost:3000, necessary for Nginx
    environment:
      MB_DB_FILE: /metabase-data/metabase.db  # Metabase metadata database
      MB_SITE_URL: http://localhost:3000/metabase/  # Metabase URL, Nginx will redirect to this
```

Run metabase locally with:

``` bash
docker-compose up -d metabase;  # metabase runs on localhost:3000
```

## Setup Nginx reverse proxy

Nginx reverse proxy will listen on port 80, and redirect the traffic from
`/metabase` to your local metabase application, running on `localhost:3000`.

Before using HTTPS, let's configure Nginx to redirect the traffic as explained
above:

``` text
server {
  server_name             domain.com;

  proxy_set_header        Host $host;
  proxy_set_header        X-Real-IP $remote_addr;
  proxy_set_header        X-Forward-For $proxy_add_x_forwarded_for;
  proxy_set_header        X-Forwarded-Proto $scheme;
  proxy_set_header Proxy  "";
  proxy_redirect          off;

  location /metabase/ {
    proxy_pass            http://localhost:3000/;
  }
}
```

Then, you can use Certbot and Let's encrypt to add HTTPS to the website. You
can follow the instructions on
[Certbot's website](https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx).
Once you're done, you will see that your nginx configuration file was edited
by certbot to add the SSL certificates. It may look something like this:

``` text
server {
  server_name             domain.com;

  proxy_set_header        Host $host;
  proxy_set_header        X-Real-IP $remote_addr;
  proxy_set_header        X-Forward-For $proxy_add_x_forwarded_for;
  proxy_set_header        X-Forwarded-Proto $scheme;
  proxy_set_header Proxy  "";
  proxy_redirect          off;

  location /metabase/ {
    proxy_pass            http://localhost:3000/;
  }

  listen [::]:443 ssl ipv6only=on; # managed by Certbot
  listen 443 ssl; # managed by Certbot
  ssl_certificate /etc/letsencrypt/live/domain.com/fullchain.pem; # managed by Certbot
  ssl_certificate_key /etc/letsencrypt/live/domain.com/privkey.pem; # managed by Certbot
  include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
```

## Conclusion

Now you should be good to go, the Metabase application should successfully
appear under https://domain.com/metabase. You can proceed to the configuration
of your databases, as explained on the [Metabase documentation](https://www.metabase.com/docs/latest/setting-up-metabase.html)

Note that we passed the `db.sqlite` database as a volume
to the docker container (in docker-compose.yml: `./db.sqlite:/db.sqlite`).
So when Metabase will ask where your sqlite database is located, you will
have to write `/db.sqlite`.

I hope this post was useful, don't hesitate to let me know in the comments.
