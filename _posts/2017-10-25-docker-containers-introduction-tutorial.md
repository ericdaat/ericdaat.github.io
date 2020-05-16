---
layout: post
title: An introduction to Docker
date: 2017-10-25
last_modified_at: 2020-05-12
excerpt:
    A tutorial on how to get started with Docker.
cover: containers.jpg
categories: ["Software Engineering"]
image: /assets/img/eric.jpg
redirect_from:
  - /blog/2017/10/25/docker/
  - /software%20engineering/2017/10/25/docker/
---

This post is a short tutorial to Docker. We will first talk about what Docker
is and how it differs fromw to get started and run your first container.

## Introduction

### About Docker

> “Docker containers wrap a piece of software in a complete filesystem that
contains everything needed to run: code, runtime, system tools, system libraries
– anything that can be installed on a server. This guarantees that the software
will always run the same, regardless of its environment.”
*Source: [Docker Website](https://www.docker.com/what-docker )*

### Advantages

Docker has some of the following advantages:

- Lightweight:
  * Containers share the same kernel (unlike Virtual Machines)
  * Use less RAM
  * Share common files (No need to duplicate files on each container)
- Open
  * Run all major Linux distributions … as well as Windows, on top of any
infrastructure
  * Can pull images from official sources (OS like Ubuntu, Debian … or even
pre-configured applications like Redis, Nginx, …)
- Secure
  * Containers isolate applications from one another

### Virtual Machines vs. Containers

- Virtual Machines include the application, necessary binaries and libraries and
entire guest OS
- Containers include application and all of its dependencies, but share the kernel!
 They can run on any computer/infrastructure/cloud

![vms-vs-containers](/assets/img/articles/docker/vm-vs-container.png)

*Source: [docker.com](https://www.docker.com/resources/what-container)*

## Installation

You will need to do 3 things:

- [Install Docker Engine](https://docs.docker.com/engine/installation/)
- [Post steps installation if you use Linux](https://docs.docker.com/engine/installation/)
- [Install Docker Compose](https://docs.docker.com/compose/install/) (*optional*)

Below are the commands you will need to install Docker Community Edition (Docker
CE) on Ubuntu/Debian.

``` bash
sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

sudo apt-get update

sudo apt-get install docker-ce

sudo docker run hello-world
```

From now on the Docker Engine is installed, but you will only be able to run it
with *sudo*, which is not ideal. To fix this, Docker provides some post
installation steps, that correspond to the following commands:

``` bash
sudo groupadd docker
sudo usermod -aG docker $USER
docker run hello-world # works without sudo!
```

I like to use Docker Compose to deploy my containers. You can specify your
containers and their configuration in a *yaml* file, and then run them all at
once. To install Docker Compose, run the following commands:

``` bash
sudo curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
```

## First steps

Let's get started and run our first container. A container runs from an image, just like an object is instanciated from an image in Object Oriented Programming. This means that before running a container, we must build or download an existing image.

Just like OOP, you don't have to start from scratch and you can use prebuilt images to get started. For instance, if you want to run a website in an apache webserver, you can use apache's docker image, and customize it to your needs. You could also start from a lower level, and use a Debian image on which you'd install apache webserver.

We said earlier that images could be built or downloaded. To build an image, you can use a Dockerfile which is a text file in which you specify the commands to build your docker image. The Dockerfile reference can be found on Docker's website following [this link](https://docs.docker.com/engine/reference/builder/). Note that this file must be named "Dockerfile" (keep the capital D).

A very simple Dockerfile may look like this:

``` text
FROM ubuntu
CMD echo "This is a test."
```

This will pull the ubuntu Docker image, run it and display "This is a test.". After this commands succeeds, the container will stop. This is very important, a container lives as long as the command assigned to it runs. This also means that you must not run more than one application per container.

In the previous example, we used ubuntu image by pulling it to our own image. A lot of pre-existing images are stored and usable by everybody. They are all available on [Docker Hub](https://hub.docker.com/explore/). You can find official images like Debian, Ubuntu, Nginx... But also images than other people built.

Here are some basic commands to get you started with Docker:

``` bash
docker build . # builds a container from a Dockerfile (using the Dockerfile is in the active directory)
docker pull debian:latest # pulls the latest version of the debian image
docker run <image-name> # runs a container from an imqge
docker ps # lists the running containers
docker ps -a # lists all the containers
docker images # lists the built images
docker rm <container-id> # removes a stopped container
docker rm -f <container-id> # force remove a container
docker rmi <image-id> # removes a built image
```

## Running your first container

Let's run an apache webserver, using the [Apache HTTP](https://hub.docker.com/r/_/httpd/) image.

``` bash
docker pull httpd:latest
```

Now you should see the httpd image when running `docker images` command.

When you run a container, you can give it several options. Let's have a look at this command:

``` bash
docker run -d -p 80:80 my_image
```

Here, we asked docker to run an image called *my_image* with the following options:

- \-d: The container runs in *detached* mode (in background)
- \-p: We are mapping the container's port 80 to our localhost:80. This means that we can access the container's application on our host. Without this option, the container would still run, but we woudldn't be able to access its application.

With such a configuration, you can open a web browser and visit *localhost*. This will display the container's apache web server content.

### Attaching volumes

Let's say we created a very cool static website in HTML/CSS, and we stored it in our *./mywebsite* local directory. So far our apache container only displays the defaut *index.html* file. How can we pass the container the awesome website we built ? There are several options, including:

- Copy the content from the host to the container when building the image. This means that the data will be stored within the image. If you save the image and pull it somewhere, you will have a copy of the data with it. If you delete the container, you delete the data. If you want to launch the same container several times, they will all have a distinct copy of the data.
- Link the data between the host and the container. This is often a preferred option. By doing this, you don't store the data within the container, you simply create a link from a folder on your host, to the container. This is called volume mapping. Doing so is much more lightweight, but requires to have the data locally. Another advantage is that if you want to run multiple containers from the same image, they can use the same data. If you change the data locally, the containers will render the newer data.

To copy data from the host to the container image, add a *COPY* command to your Dockerfile, like so:

``` text
FROM httpd
COPY ./mywebsite/:/usr/local/apache2/htdocs/
```

To link a volume, add the *-v* option to the *run* command:

``` bash
docker run -d -p 80:80 -v ./mywebsite/:/usr/local/apache2/htdocs/ httpd
```

Voila! Your container should now be running an apache web server in detached mode. And since we mapped the volume containing our awesome website, what you see on *localhost* is exactly what we have under the local *./mywebsite* directory.

### Docker Compose

Often, you will need to build and run many different containers, and using the previously seen commands for each container can become very dull. In this section we will introduce Docker Compose, which is a very handy tool for defining and running multiple containers from a YAML configuration file. Here is how this file might look like for the apache webserver we had before.

``` yaml
version: '3'
services:
  website:
   image: httpd:latest
   ports:
    - 80:80
   volumes:
    - ./mywebsite/:/usr/local/apache2/htdocs/
```

### Linking containers

Now imagine you are running a web application in a container, and you need access to various services such as a relational database and a cache server. These three services can be run in different containers talking to each others via links. You might notice the *expose* keyword. Containers by default have all their ports closed. We previously seen that we could map a container's port to the host by using *ports*. Thanks to *expose*, we tell a container to open its port to other containers. Exposing a container's port does not make it accessible from the host.

``` yaml
version: '3'
services:
  website:
   image: httpd:latest
   ports:
    - 80:80
   volumes:
    - ./mywebsite/:/usr/local/apache2/htdocs/
   links:
    - redis
  cache:
   image: redis:latest
   expose:
    - 6379
```

This post is certainly not exhaustive. It is just a quick introduction to Docker, and I emphasized on commands and practices I am using most of the time. Of course Docker has a very large number of additional functionnalities, and you should explore them while you work with containers. I hope this post was useful to get you started.
