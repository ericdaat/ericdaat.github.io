---
layout: post
title: Installing Tensorflow with GPU support on Linux
date: 2018-01-16
excerpt:
    Lately I spent some time using Deep Learning and configuring Linux servers with GPUs so the models train faster. In this short blog post I am going to list all what you have to follow in order to properly install the nvidia drivers, cuda, and other tools you'll need before running Tensorflow (or Keras) with GPU support. Let's get to it !
cover: server.jpg
---

Lately I spent some time using Deep Learning and configuring Linux servers with GPUs so the models train faster. In this short blog post I am going to list all what you have to follow in order to properly install the nvidia drivers, cuda, and other tools you'll need before running Tensorflow (or Keras) with GPU support.

Note that this tutorial can work either on Ubuntu or Debian. This tutorial will install `tensorflow-gpu 1.12` which
is the latest version available while I am writing these words.

Tensorflow GPU needs the following softwares:

- NVIDIA® GPU drivers (CUDA 9.0 requires 384.x or higher)
- CUDA® Toolkit (TensorFlow supports CUDA 9.0)
- cuDNN SDK (>= 7.2)

## Installing on Ubuntu

Here is a complete shell script showing the different steps to install `tensorflow-gpu`:

``` bash
# Guide for installing Tensorflow on Ubuntu 16.04

# Requirements
# From Tensorflow GPU docs (https://www.tensorflow.org/install/gpu):
# The following NVIDIA® software must be installed on your system:

# NVIDIA® GPU drivers —CUDA 9.0 requires 384.x or higher.
# CUDA® Toolkit —TensorFlow supports CUDA 9.0.
# CUPTI ships with the CUDA Toolkit.
# cuDNN SDK (>= 7.2)
# (Optional) NCCL 2.2 for multiple GPU support.
# (Optional) TensorRT 4.0 to improve latency and throughput for inference on some models.


# Check your device has GPUs
lspci | grep -i nvidia;

# Login as root (so you don't have to write sudo all the time)
su;

# install GCC
apt-get install gcc;
apt-get install build-essential;
gcc --version; # check that it has been installed correctly
apt-get install linux-headers-$(uname -r);

# Nvidia drivers, v384
wget http://us.download.nvidia.com/tesla/384.183/NVIDIA-Linux-x86_64-384.183.run;
chmod +x NVIDIA-Linux-x86_64-384.183.run;
./NVIDIA-Linux-x86_64-384.183.run;

# CUDA v9.0
wget https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run;
chmod +x cuda_9.0.176_384.81_linux-run;
./cuda_9.0.176_384.81_linux-run; # also install the cuda toolkit

# CUDNN 7.5
# Get the .tgz file from here: https://developer.nvidia.com/rdp/cudnn-download
scp cudnn-9.0-linux-x64-v7.5.0.56.tgz USER@IP:/path/to/your/dir;
tar -xzvf cudnn-9.0-linux-x64-v7.5.0.56.tgz;
cp -P cuda/include/cudnn.h /usr/local/cuda/include;
cp -P cuda/lib64/libcudnn* /usr/local/cuda/lib64;
chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda-9.0/lib64/libcudnn*;

# Append these two lines to your .bashrc
export PATH=/usr/local/cuda/bin:$PATH
export CUDA_HOME=/usr/local/cuda;
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
source .bashrc;

# Actual Tensorflow install
apt-get update;
apt-get install python3-dev python3-pip;
pip3 install -U virtualenv;  # system-wide install
virtualenv --system-site-packages -p python3 ./venv;
source ./venv/bin/activate  # sh, bash, ksh, or zsh;
pip install tensorflow-gpu;

# Verify the install
python -c "import tensorflow as tf; tf.enable_eager_execution(); print(tf.reduce_sum(tf.random_normal([1000, 1000])))"
```

## Docker Image

If you are familiar with [Docker](https://www.docker.com/), I'd recommend you have a look at the [Tensorflow Docker Image](https://hub.docker.com/r/tensorflow/tensorflow/). It's already configured with the latest drivers and can run on CPU or GPU.

If you're not familiar with Docker, you should definitely learn using it. Here are some links to get you started:

- [My introduction to Docker blog post](https://ericdaat.github.io/docker-introduction.html)
- [Docker official website](https://www.docker.com/)
- [Docker getting started guide](https://docs.docker.com/get-started/)

### Install Keras on top of Tensorflow

This step is not required, and some people probably prefer using Tensorflow directly with no abstraction layer on top of it. I personally started doing Deep Learning with Keras on top of Tensorflow, because it provided a simpler API, and I find it really easy and fast to build models.
Keras was build by [François Chollet](https://twitter.com/fchollet?lang=en), and since he is now working for Google, Keras is very well integrated with Tensorflow.

Installing keras is as easy as `pip install keras`. It will automatically detect your GPUs if you have `tensorflow-gpu` installed, like we did.

To get started, have a look at the official [Keras website](https://keras.io/) and their [getting started guide](https://keras.io/#getting-started-30-seconds-to-keras). I have also wrote a blog post with some [Keras snippets](https://ericdaat.github.io/keras-snippets.html) that I find useful.

I hope this post was helpful, and have fun with Deep Learning !

<iframe src="https://giphy.com/embed/W9zNtyI9I4lG" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/neural-networks-W9zNtyI9I4lG">via GIPHY</a></p>
