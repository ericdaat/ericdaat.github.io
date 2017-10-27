Title: An introduction to Docker
Date: 2017-10-25 10:20
Modified: 2017-10-25 10:20
Category: Programming
Tags: docker, code, devops
Authors: Eric Daoud
Slug: docker-introduction
Summary: A tutorial on how to get started with Docker.
Status: published

# Introduction
## What is Docker ?
> “Docker containers wrap a piece of software in a complete filesystem that
contains everything needed to run: code, runtime, system tools, system libraries
– anything that can be installed on a server. This guarantees that the software
will always run the same, regardless of its environment.”  
*Source: [Docker Website](https://www.docker.com/what-docker )*

## Advantages
Docker has some of the following advantages:

 - Lightweight
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

## Virtual Machines vs. Containers

 - Virtual Machines include the application, necessary binaries and libraries and
entire guest OS
 - Containers include application and all of its dependencies, but share the kernel!
 They can run on any computer/infrastructure/cloud

![vms-vs-containers](https://www.docker.com/sites/default/files/containers-vms-together%402x.png)

# Installation
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

# First steps
