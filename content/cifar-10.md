Title: Playing with ConvNets on CIFAR-10 dataset
Date: 2018-01-24 10:20
Modified: 2018-01-24 10:20
Category: Programming
Tags: keras, code, deep-learning
Slug: deep-learning-convnets-cifar
Authors: Eric Daoud
Summary: ConvNets related post
Status: published

## The Dataset

You can find the CIFAR-10 Dataset on the University of Toronto [website](https://www.cs.toronto.edu/~kriz/cifar.html). I used [CIFAR-10 python dataset](https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz) for my study.

After extracting the archive, you will have a folder containing serveral files, including:

 - `data_batch[1-5]`: pickled training data. Each batch contains 10,000 samples.
 - `test_batch`: pickled test data

A training batch, once unpickled, consists in a python dictionary, formatted as such:

 - data: a numpy array of shape $10000 \times 3072$ where 10,000 is the number of samples and 3072 is the RGB pixels values combined.
 - labels: a python list of length 10000 representing the class index, from 0 to 9.
 - batch\_label: the name of the training batch.
 - filenames: the corresponding picture filename.

``` python
{'data': array([[ 35,  27,  25, ..., 169, 168, 168],
 'labels' [1, 6, 6, ..., 6, 0, 6],
 'batch_label': 'training batch 1 of 5',
 'filenames': ['auto_s_000241.png', ..., 'rana_catesbeiana_s_000111.png']}
```


## Full Code

``` python
import cPickle
import os
from glob import glob
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard, ReduceLROnPlateau
from keras.optimizers import Adam


def unpickle(file):
    with open(file, 'rb') as fo:
        dict = cPickle.load(fo)
    return dict


def parse_image(row):
    r = row[:1024]
    g = row[1024:2048]
    b = row[2048:]

    return np.asarray([r, g, b]).T.reshape(32, 32, 3)


data = []
labels = []

for fname in glob('./cifar-10-batches-py/data_batch_[0-9]'):
    pkl = unpickle(fname)
    data_ = pkl['data']
    labels_ = np.asarray(pkl['labels']).reshape(-1, 1)

    data.append(np.asarray(map(parse_image, data_)))
    labels.append(np.asarray(labels_))

X = np.vstack(np.asarray(data))
y = np.vstack(np.asarray(labels))

del data
del labels

X_train, X_test, y_train, y_test = train_test_split(X, y)
print X_train.shape, y_train.shape, X_test.shape, y_test.shape

model = Sequential()
model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 activation='relu',
                 padding='same',
                 input_shape=(32, 32, 3)))
model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 activation='relu',
                 padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(filters=64,
                 kernel_size=(3, 3),
                 activation='relu',
                 padding='same',))
model.add(Conv2D(filters=64,
                 kernel_size=(3, 3),
                 activation='relu',
                 padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(10, activation='softmax'))

adam = Adam(lr=0.0001)

model.compile(loss='sparse_categorical_crossentropy',
              optimizer=adam,
              metrics=['sparse_categorical_accuracy'])

tensorboard = TensorBoard(log_dir='/home/manomano/tensorboard-logs/cifar-10')
reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                              factor=0.2,
                              patience=5,
                              min_lr=0.00001)

model.fit(X_train,
          y_train,
          validation_data=(X_test, y_test),
          batch_size=128,
          epochs=240,
          callbacks=[tensorboard, reduce_lr])
```
