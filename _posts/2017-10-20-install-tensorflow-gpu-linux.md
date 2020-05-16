---
layout: post
title: Installing Tensorflow with GPU support on Linux
date: 2018-01-16
last_modified_at: 2020-05-12
excerpt:
    Lately I spent some time using Deep Learning and configuring Linux servers with GPUs so the models train faster. In this short blog post I am going to list all what you have to follow in order to properly install the nvidia drivers, cuda, and other tools you'll need before running Tensorflow (or Keras) with GPU support. Let's get to it !
cover: server.jpg
categories: ["Machine Learning"]
image: /assets/img/eric.jpg
redirect_from:
    - /machine%20learning/2017/12/16/keras-snippets/
    - /blog/2018/01/16/install-tensorflow-gpu/
---

Note that this tutorial can work either on Ubuntu or Debian.
This tutorial will install `tensorflow-gpu 1.12` which
is the latest version available while I am writing these words.

Tensorflow GPU needs the following softwares:

- NVIDIA® GPU drivers (CUDA 9.0 requires 384.x or higher)
- CUDA® Toolkit (TensorFlow supports CUDA 9.0)
- cuDNN SDK (>= 7.2)

## Installing on Ubuntu

Here is a complete shell script showing the different steps to install `tensorflow-gpu`:

{% gist 8623e2e1e0b80f6a94eeedeecd80828d %}

## Docker Image

If you are familiar with [Docker](https://www.docker.com/), I recommend you have a look at the [Tensorflow Docker Image](https://hub.docker.com/r/tensorflow/tensorflow/). It's already configured with the latest drivers and can run on CPU or GPU.

If you're not familiar with Docker, you should definitely learn using it. Here are some links to get you started:

- [My introduction to Docker blog post](/blog/2017/10/25/docker/)
- [Docker official website](https://www.docker.com/)
- [Docker getting started guide](https://docs.docker.com/get-started/)

### Install Keras on top of Tensorflow

This step is not required, and some people probably prefer using Tensorflow directly with no abstraction layer on top of it. I personally started doing Deep Learning with Keras on top of Tensorflow, because it provided a simpler API, and I find it really easy and fast to build models.
Keras was build by [François Chollet](https://twitter.com/fchollet?lang=en), and since he is now working for Google, Keras is very well integrated with Tensorflow.

Installing keras is as easy as `pip install keras`. It will automatically detect your GPUs if you have `tensorflow-gpu` installed, like we did.

To get started, have a look at the official [Keras website](https://keras.io/) and their [getting started guide](https://keras.io/#getting-started-30-seconds-to-keras). I have also wrote a blog post with some
[Keras snippets](/blog/2017/12/16/keras-snippets/)
that I find useful.

I hope this post was helpful, and have fun with Deep Learning !

<iframe src="https://giphy.com/embed/W9zNtyI9I4lG" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/neural-networks-W9zNtyI9I4lG">via GIPHY</a></p>
