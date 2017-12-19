Title: Some Keras snippets
Date: 2017-12-16 10:20
Modified: 2017-12-16 10:20
Category: Programming
Tags: python, keras, code, deep-learning
Slug: keras-snippets
Authors: Eric Daoud
Summary: Some Keras snippets
Status: published


# Networks example


## Regression

``` python
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot
import numpy as np
from IPython.display import SVG

X = np.random.rand(200, 10)
y = np.random.rand(200, 1)

model = Sequential()
model.add(Dense(1, activation='relu', input_shape=(10,)))
model.compile('sgd', 'mse')

# SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))
plot_model(model, to_file='regression.png')

model.fit(X, y, epochs=5)
model.predict(np.random.rand(1, 10))
```


## Binary Classification

``` python
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot
import numpy as np
from IPython.display import SVG

X = np.random.rand(200, 10)
y = np.random.randint(0, 2, 200)

model = Sequential()
model.add(Dense(1, activation='relu', input_shape=(10,)))
model.compile('sgd', 'binary_crossentropy')

# SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))
plot_model(model, to_file='binary_classifier.png')

model.fit(X, y, epochs=5)
model.predict(np.random.rand(1, 10))
```


## Multiclass Classification

``` python
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot
import numpy as np
from IPython.display import SVG

X = np.random.rand(200, 10)
y = np.random.randint(0, 100, 200)
y = to_categorical(y) # no need for this line if you
                      # use 'sparse_categorical_crossentropy' loss
                      # during compile

model = Sequential()
model.add(Dense(100, activation='softmax', input_shape=(10,)))
model.compile('sgd', 'categorical_crossentropy')

# SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))
plot_model(model, to_file='multiclass_classifier.png')

model.fit(X, y, epochs=5)
model.predict(np.random.rand(1, 10))
```


## Embeddings

``` python
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot
import numpy as np
from IPython.display import SVG

X = np.random.randint(1000, size=(200, 10))
y = np.random.randint(0, 100, 200)
y = to_categorical(y) # no need for this line if you
                      # use 'sparse_categorical_crossentropy' loss
                      # during compile

model = Sequential()
model.add(Embedding(input_dim=1000,
                    output_dim=64,
                    input_length=10))
model.add(Flatten()) # will stack each word embedding
model.add(Dense(100, activation='softmax'))
model.compile('sgd', 'categorical_crossentropy')

# SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))
plot_model(model, to_file='embeddings_classifier.png')

model.fit(X, y, epochs=5)
model.predict(np.random.rand(1, 10))
```


## Embeddings with the functional API


``` python
from keras.models import Model
from keras.layers import Dense, Embedding, Lambda, Input
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot
import numpy as np
from IPython.display import SVG

X = np.random.randint(1000, size=(200, 10))
y = np.random.randint(0, 100, 200)

x = Input(shape=(10,), dtype='int32')
h = Embedding(output_dim=64, input_dim=1000)(x)
h = Lambda(lambda r: mean(r, axis=1))(h)
o = Dense(100, activation='softmax')(h)

model = Model(inputs=[x], outputs=[o])
model.compile('sgd', 'sparse_categorical_crossentropy')

# SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))
plot_model(model, to_file='embeddings_classifier_functional.png')

model.fit(X, y, epochs=5)
model.predict(np.random.rand(1, 10))
```


## Handling multiple inputs

``` python
from keras.models import Model
from keras.layers import Dense, Embedding, Lambda, Input, concatenate
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot
import numpy as np
from IPython.display import SVG

X1 = np.random.randint(1000, size=(200, 10))
X2 = np.random.randint(1000, size=(200, 10))
X3 = np.random.randint(1000, size=(200, 10))
y = np.random.randint(0, 100, 200)

x1 = Input(shape=(10,), dtype='int32')
x2 = Input(shape=(10,), dtype='int32')
x3 = Input(shape=(10,), dtype='int32')
h1 = Embedding(output_dim=64, input_dim=1000)(x1)
h1 = Lambda(lambda r: mean(r, axis=1))(h1)
h2 = Embedding(output_dim=64, input_dim=1000)(x2)
h2 = Lambda(lambda r: mean(r, axis=1))(h2)
h3 = Embedding(output_dim=64, input_dim=1000)(x3)
h3 = Lambda(lambda r: mean(r, axis=1))(h3)
h = concatenate([h1, h2, h3])
o = Dense(100, activation='softmax')(h)

model = Model(inputs=[x1, x2, x3], outputs=[o])
model.compile('sgd', 'sparse_categorical_crossentropy')

# SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))
plot_model(model, to_file='multi_embeddings_classifier_functional.png')

model.fit([X1, X2, X3], y, epochs=5)
model.predict([np.random.rand(1, 10),
               np.random.rand(1, 10),
               np.random.rand(1, 10)])
```


# Callbacks

``` python
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot
from keras.callbacks import TensorBoard, History, EarlyStopping
import numpy as np
from IPython.display import SVG

X = np.random.rand(200, 10)
y = np.random.rand(200, 1)

model = Sequential()
model.add(Dense(1, activation='relu', input_shape=(10,)))
model.compile('sgd', 'mse')

# SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))
plot_model(model, to_file='regression.png')

history = History()
tensorboard = TensorBoard(log_dir='./logs/run1')

model.fit(X,
          y,
          epochs=5,
          callbacks=[history, tensorboard])

model.predict(np.random.rand(1, 10))

# history.history
# start tensorboard with tensorboard --logdir=run1:./logs/run1
```
