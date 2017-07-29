Title: Deploying a Python Flask application to production
Date: 2017-05-28 10:20
Modified: 2017-05-28 10:20
Category: Programming
Tags: python, code
Slug: deploy-python-flask-api
Authors: Eric Daoud
Summary: In this post we are going to see how we can efficiently deploy a web application powered by Flask (a Python framework) to production. We won't code a complex application, actually we will just stick to the Flask Hello World example.
Status: draft


In this post we are going to see how we can efficiently deploy a web application powered by Flask (a Python framework) to production. We won't code a complex application, actually we will just stick to the Flask Hello World example.


## Basic Flask application
If you've never heard of Flask before, I recommend you to visit the [website](#) and read about it.

To create a Hello World application in Flask, just write the following code in a file called ```application.py```.

``` python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello, World!"
```

And then run the application with this code in a ```main.py``` file.

``` python
from application import app as application

if __name__ == '__main__':
	application.run()
```

Now run ```python main.py``` and your app should be visible in your browser at ```localhost:5000```.


## WSGI server
So far we have a working application, but it won't be enough to serve a production environment. Python applications can't be directly deployed in a webserver, because python is not a web compatible language like Javascript or PHP for instance. Hence, we need an additional layer: a WSGI server.

There are various WSGI servers on the market, [Gunicorn](#) is a popular choice but my favorite is [uWSGI](#).

### Getting started

You can install uWSGI with pip: ```pip install uwsgi```. Once you have it installed, you can run our previous python application within a WSGI webserver by simply doing ```uwsgi main.py```. You can pass many arguments to the ```uwsgi``` command, but it is often prefered to have them all in a single configuration file. uWSGI can just do that, let's create a ```uwsgi.ini``` configuration file that looks like this:

``` text
[uwsgi]
wsgi-file = main.py
master = true
processes = 2
http = 0.0.0.0:9000
vacuum = true
die-on-term = true
```

Now we can run the app with ```uwsgi wsgi.ini```. With such configuration, our Flask application will be hosted on 2 processes. This is an arbiratry number we set, but you can increase it either manually or automatically if you need to handle more trafic. The server will respond on ```0.0.0.0:9000```, which means that every client on the local network will be able to access the app on port 9000 using the HTTP protocol. Check that you can still see your app at ```localhost:9000```. You should also be able to see it from another device connected to the same network at ```<your-ip>:9000```.


## Putting uWSGI behing NGINX reverse proxy
The document from uWSGI states that you should use uWSGI behind a reverse proxy such as NGINX. This is fairly easy with this configuration file:

``` text
upstream backend {
    least_conn;
    server localhost:9000;
}

server {
    listen 80;
    location {
    	uwsgi_pass backend;
        include uwsgi_params;
    }
}
```

With such a configuration, NGINX listens on port 80 and redirects the requests to ```localhost:9000``` which is our uwsgi server. Be careful though, since we use ```uwsgi_pass``` command, the uwsgi application must run in a socket and not on http. Just change your ```uwsgi.ini``` configuration file accordingly:

``` text
[uwsgi]
wsgi-file = main.py
master = true
processes = 2
socket = 0.0.0.0:9000
vacuum = true
die-on-term = true
```

## Run NGINX and uWSGI in Docker
I love [Docker](#), and I tend to use it more and more for about everything I build. To run this python application, I chose to build two containers, one for NGINX reverse proxy and one for our uWSGI application. I personnally run my Docker containers with [docker-compose](#), that makes it easy to configure multiple containers.

```text
FROM python:2.7
MAINTAINER eric <eric@eric.com>

RUN pip install flask uwsgi

RUN useradd -ms /bin/bash flask-app
USER flask-app
WORKDIR /home/flask-app

EXPOSE 9000
CMD uwsgi uwsgi.ini
```

```text
version: '2'
services:
	flask-app:
		build: ./flask-app
		volumes:
			- ./flask-app:/home/flask-app
		logging:
			driver: "json-file"
			options:
			max-size: "10m"
			max-file: "2"
 	nginx:
 		image: nginx:latest
 		volumes:
 			- ./nginx.conf:/etc/nginx/nginx.conf
```


