Title: Installing Tensorflow with GPU support on Linux (Debian)
Date: 2018-01-16 10:20
Modified: 2018-01-16 10:20
Category: Programming
Tags: tensorflow, keras, code, config, server, deep-learning
Slug: install-tensorflow-gpu
Authors: Eric Daoud
Summary: Lately I spent some time using Deep Learning and configuring Linux servers with GPUs so the models train faster. In this short blog post I am going to list all what you have to follow in order to properly install the nvidia drivers, cuda, and other tools you'll need before running Tensorflow (or Keras) with GPU support. Let's get to it !
Status: published

Lately I spent some time using Deep Learning and configuring Linux servers with GPUs so the models train faster. In this short blog post I am going to list all what you have to follow in order to properly install the nvidia drivers, cuda, and other tools you'll need before running Tensorflow (or Keras) with GPU support. Let's get to it !

# Installing Nvidia Graphic Drivers and Cuda

For this part, I followed instructions from the [Debian Wiki](https://wiki.debian.org/NvidiaGraphicsDrivers).

``` bash
echo "deb http://httpredir.debian.org/debian/ stretch main contrib non-free" /etc/apt/sources.list
apt update
apt install linux-headers-$(uname -r|sed 's/[^-]*-[^-]*-//') nvidia-driver
apt install nvidia-xconfig

reboot

apt-get install nvidia-cuda-dev nvidia-cuda-toolkit  nvidia-driver
```

# Installing Cudnn

For this part, you're going to need to register as an Nvidia Developer. Then, download Cuda v6 (Tensorflow needs this version, at least it does while I'm writing these lines) from the [Nvidia Developer Website](https://developer.nvidia.com/rdp/cudnn-download)

``` bash
cd /home/user
tar xvzf cudnn-8.0-linux-x64-v6-ga.tgz
mkdir /usr/local/cuda
mkdir /usr/local/cuda/include
mkdir /usr/local/cuda/lib64
cp -P cuda/include/cudnn.h /usr/local/cuda/include
cp -P cuda/lib64/libcudnn* /usr/local/cuda/lib64
chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*

echo "export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"" > .bashrc
echo "export CUDA_HOME=/usr/local/cuda" > .bashrc

apt-get install libcupti-dev
```

# Installing Python and virtualenv

This part is the easiest. You can see more details on the [Tensorflow](https://www.tensorflow.org/install/install_linux#InstallingVirtualenv) page.

``` bash
apt-get install python python-pip
virtualenv tensorflow
source tensorflow/bin/activate
pip install tensorflow-gpu
```

Et voila ! You should be able to run Tensorflow using GPUs on your Linux server. Just make sure it works by running this simple program:

``` python
# Python
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```

<iframe src="https://giphy.com/embed/W9zNtyI9I4lG" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/neural-networks-W9zNtyI9I4lG">via GIPHY</a></p>
