---
layout: post
title: Python Tips and Tools
date: 2017-05-28
excerpt:
    There are a few Python things I learnt over the years, and I decided to share them in this post. I'll cover the basis of Object Oriented Programming; then some useful functions or tools that I like about the language; finally, I'll speak about how to organise a project and install libraries with virtual environments.
cover: code.jpg
---

I love Python programming language, and I have been using it for several years now. It is a very simple yet powerful language that is used for so many purposes. It is quite an old language created by Guido Van Rossum in 1989 ... when he was bored !

>*Over six years ago, in December 1989, I was looking for a "hobby" programming project that would keep me occupied during the week around Christmas. My office ... would be closed, but I had a home computer, and not much else on my hands. I decided to write an interpreter for the new scripting language I had been thinking about lately: a descendant of ABC that would appeal to Unix/C hackers. I chose Python as a working title for the project, being in a slightly irreverent mood (and a big fan of Monty Python's Flying Circus).
> -- Guido Van Rossum, 1996*

There are a few Python things I learnt over the years, and I decided to share them in this post. I'll cover the basis of Object Oriented Programming; then some useful functions or tools that I like about the language; finally, I'll speak about how to organise a project and install libraries with virtual environments. Before we dive in this article, let me mention a few things:

1. This is absolutely not exhaustive. I am very aware that I don't know all about Python and have no legitimacy teaching it. I just wanted to share some of my favorite aspects of the language.
2. You can learn more about Python [here](https://www.python.org/).
3. I personally started learning it by reading [Learn Python the Hard Way](https://learnpythonthehardway.org/book/)
4. For Mac users, it is recommended to **not** use the built in macOS Python. Instead, do the following:
    - Get [Homebrew](https://brew.sh/), the missing package manager for macOS
    - Run `brew install python`

## Object Oriented Programming

A python code doesn't need to be Object Oriented, as opposed to Java for instance: It can be used as a scripting language. However in many projects you will need classes and methods. This section will explain how to write Object Oriented code in Python. Note that this assumes that you know of Object Oriented Programming, I am not going to explain the theory behind it. If you are not familiar with it, I recommended checking out this [Wikipedia](https://en.wikipedia.org/wiki/Object-oriented_programming) post.

### Simple Class

We create a basic class `MyClass` with a constructor `__init__` that takes no argument. Our class is very simple and has no attribute. Note that `self` is just a keyword, it serves as a placeholder for the instance object.

``` python
class MyClass(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    my_class = MyClass()    # call to the __init__ constructor
```

### Passing arguments

Let's improve our class by changing the constructor and adding arguments. Arguments in the constructor (or in any method) go after the `self` keyword.

``` python
class MyClass(object):
    def __init__(self, arg):
        self.arg = arg

if __name__ == '__main__':
    my_class = MyClass(1)   # call to the __init__ constructor
    print my_class.arg      # will print 1
```

Note that unlike Java, you can't define multiple constructors for one same class:

``` python
class MyClass(object):
    def __init__(self, arg):
        self.arg = arg

    def __init__(self): # this will not work, since we already defined a constructor
        self.arg = 1
```

### Calling methods

We can now add an instance method to our class. Such a method must always have `self` as first argument. Later, we will talk about instance methods versus class methods and see how they differ.

``` python
class MyClass(object):
    def __init__(self, arg):
        self.arg = arg

    def some_method(self, value):
        return value

if __name__ == '__main__':
    my_class = MyClass(1)
    print my_class.some_method(3)      # will print 3
```

### Inheritance

Here we create two Classes `A` and `B`, where `B` inherits from `A`. Notice how `B` can use `a_method` even though it is defined in `A`. Indeed, a subclass has access to every method and attribute from its superclass.

``` python
class A(object):
    def __init__(self, arg):
        self.arg = arg

    def a_method(self, value):
        return value

class B(A):
    def __init__(self, arg):
        super(B, self).__init__(arg)    # calls A constructor with arg

if __name__ == '__main__':
    b = B(1)                            # creates A then B
    print b.a_method(3)                 # will print 3
```

### Overidding

A subclas can redefine its superclass behavior. This is called overidding. Here we have the same `A` and `B` Classes, but this time we override `A.a_method` in `B` to no longer return `value`but `2 * value`.

``` python
class A(object):
    def __init__(self, arg):
        self.arg = arg

    def a_method(self, value):
        return value

class B(A):
    def __init__(self, arg):
        super(B, self).__init__(arg)    # calls A constructor with arg

    def a_method(self, value):          # overriding a_method
        return value * 2

if __name__ == '__main__':
    b = B(1)                            # creates A then B
    print b.a_method(3)                 # will print 6
```

### instance method vs. Class method

An instance method is called on an instance of the Class. Here, `Animal` is our class, and `bob` is an instance of `Animal`.

``` python
class Animal(object):
    def __init__(self, name):
        self.name = name

    def say_my_name(self):
        return self.name

if __name__ == '__main__':
    bob = Animal("Bob")
    print bob.say_my_name()      # will print "Bob"
```

A Class method however, is called on the Class itself.

``` python
class Animal(object):
    def __init__(self, name):
        self.name = name

    @classmethod
    def introduce(cls):
        return "I am {0}".format(cls)

    def say_my_name(self):
        return self.name

if __name__ == '__main__':
    print Animal.introduce()    # will print "I am <class '__main__.Animal'>"
```

### instance attribute vs. Class attribute

Similarly, we could define class attributes and instance attributes. Instance attributes belong to the instance, and are not accessible from an instance to another. However class attributes are shared by all instances of the class. It can be handy to count how many objects from one class we created.

``` python
class Animal(object):
    count = 0

    def __init__(self):
        Animal.count += 1

if __name__ == '__main__':
    animal_1 = Animal()
    animal_2 = Animal()
    animal_3 = Animal()

    print Animal.count    # will print 3
```

### Public vs. private

Methods and attributes are public by default in python. Adding a `_` makes them private:

- `self.name` vs. `self._name` for attributes
- `def some_method(self)` vs. `def _some_method(self)` for methods

``` python
class Animal(object):
    def __init__(self, name, credit_card_code):
        self.name = name
        self._credit_card_code = credit_card_code

    def _do_something_private(self):
        pass

if __name__ == '__main__':
    bob = Animal("Bob", 1234)
    print bob.name                  # will print "Bob"
    print bob.credit_card_code      # will crash
    bob.do_something_private()      # will crash
```

Note that privacy doesn't really exist in Python. Indeed, you could call `bob._do_something_private()` and it would work. Defining private methods like this is more a convention than anything else. We just give another name to the private methods and attributes.

You might also come accross `__do_something_private() declaration of methods. The two leading underscores mean that this function must not be overridden by any subclass.

### Accessing private attributes: getter & setter

When defining private attributes, we can access them with getters, and redefine them with setters.

``` python
class SomeClass(object):
    def __init__(self, value):
        self._private_attribute = value

    @property
    def private_attribute(self):
        return self._private_attribute

    @private_attribute.setter
    def private_attribute(self, new_value):
        self._private_attribute = new_value

if __name__ == '__main__':
    c = SomeClass(1)
    print c.private_attribute     # will print 1
    c.private_attribute = 2
    print c.private_attribute     # will print 2
```

That's about it for Object Oriented Programming. Knowing these little snippets, you should be able to build a decent Object Oriented Program. Don't hesitate to learn more on the subject, as this post is not exhaustive.

## Useful tools and functions

Now I'd like to show you some of my favorite python tools and handy functions. We often hear people asking for a "pythonic" way to do something, and it sometimes refer to taking advantage of some python built in tools that makes it so easy to use and elegant to read. The following paragraphs will demonstrate some of these techniques.

### Comprehension lists

Comprehension lists allow creating arrays faster and in a more much more elegant way. The first approach one might think of for creating an array in python would be to declare an empty one and then append some values to it, like in this snippet:

``` python
# The normal way:
l = []
for i in xrange(5):
"""
You should use xrange instead of range in
python2 as it avoids load an entire array in memory.
In python3, xrange is implicitly used when typing range.
"""
    l.append(i)
# l = [0, 1, 2, 3, 4]
```

It turns out that there is a simpler way to write this, and that is also more efficient:

``` python
# The list comprehension way:
l = [i for i in xrange(5)]
# l = [0, 1, 2, 3, 4]
```

It works with other Python data structures, like `dict` for instance:
``` python
# Works with dicts too !
d = {str(i):i for i in xrange(5)}
# d = {'1': 1, '0': 0, '3': 3, '2': 2, '4': 4}
```

### Enumerate

`enumerate` provides an elegant way to go through over an iterable object while keeping track of the curent item and its position.

``` python
l = [10, 20, 30]

# The normal way:
for i in xrange(len(l)):
    print i, l[i]               # will print 0, 10 then 1, 20 etc ...


# The enumerate way:
for i, item in enumerate(l):    # enumerate(l) = [(0, 10), ...]
    print i, item               # print the same thing, but nicer !
```

### Map functions

Apply a function to every item of an iterable object (e.g. arrays). Maps are faster than doing a for loop over the iterrable object.

``` python
l = [1, 2, 3]           # l is an iterable object

def f(value):           # function to apply to l items
    return 2 * value


# The normal way:
new_l = []
for i in range(len(l)):
    new_l.append(f(l))
# new_l = [2, 4, 6]


# The map way:
new_l = map(f, l)
# new_l = [2, 4, 6]

```

### Lambda functions

`lambda` functions allow to define anonymous functions, typically used when the operation to perform is really simple and doesn't need a dedicated function to be created.

``` python
l = [1, 2, 3]

def f(value):
    return 2 * value

print map(f, l)
```

Do we really need to declare a function for such an easy operation ? Nope:

``` python
l = [1, 2, 3]

print map(lambda r: r*2, l)     # will print [2, 4, 6]
```

### Partial functions

Functions used in map can only take a single argument. What if we have more ? Here, we learn to create a partial function filled with some constant arguments and leave one free, so we can map values on it.

``` python
from functools import partial

l = [1,2,3]

def f(value, coefficient):
    return value * coefficient

fp = partial(f, coefficient=2)      # fp = f(value, coefficient=2)

print map(fp, l)                    # will print [2, 4, 6]

```

### Multiprocessing with Pool

Multi process a function with multiprocessing.Pool is really easy:

``` python
from multiprocessing import Pool
import time

def f(value):
    time.sleep(1)
    return value

l = [1, 2, 3, 4]
p = Pool(4)         # say we have 4 cores --> 4 processes

map(f, l)           # would take 4 seconds (call to f(1), then f(2), then f(3), then f(4))
p.map(f, l)         # would take 1 second (simultaneously call f(1), f(2), f(3) and f(4))
```

### Handling Exceptions: with try & except

When things get unpredictive, you can avoid your program crashing by adding `try` and `except` keywords. In this snippet, `l + 1` will raise an error when l will be assigned None, as we can't add an integer and a NoneType object.

``` python
l = [1, 2, 3, None]

for i, item in enumerate(l):
    print l + 1     # will crash when item=None
```

We can handle such exceptions as follows:

``` python
l = [1, 2, 3, None]

for i, item in enumerate(l):
    try:
        print l + 1
    except:     # Will catch any exception (KeyError, ValueError, etc...)
        print "Something went wrong"
```

See the full list of Exceptions [here](https://docs.python.org/2/library/exceptions.html#bltin-exceptions).

### Assertions

`assert` checks a boolean expression and raises an exception when the expression result is False.

``` python
assert(2>=1)     # works
assert(2<=1)     # raises AssertionError
```

This can be useful for parameter checking:

```python
def f(value):
    try:
        assert(isinstance(value, int))
    except AssertionError:
        raise ValueError("value must be integer")

    return value + 1

if __name__ == "__main__":
    print f(2)      # will print 3
    print f("hi")   # will raise ValueError
```

### Loop statements

Here are some keywords that can be used within a python loop:

- `break`: terminates the current loop
- `continue`: returns to the top of the loop, ignoring future statements
- `pass`: when a statement is required, but we don't want to do anything
- `else`:
    1. in for loops, executed when the loop is done iterrating the list
    2. in while loops, executed when the condition becomes False

``` python
for i in range(10):
    if i == 5:
        break
    print i

# will print i from 0 to 4
```

``` python
for i in range(10):
    if i == 5:
        continue
    print i

# will print i from 0 to 4 and 6 to 9
```

``` python
for i in range(10):
    if i == 5:
        pass
    print i

# will print i from 0 to 9
```

``` python
for i in range(10):
    if i == 5:
        pass
    print i
else:
    print "done"

# will print i from 0 to 9, then "done"
```

### Logging

Are you using `print` for logging ? Stop right now, and consider using the built in `logging` module which makes it really easy to display and organise your logs.

``` python
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG     # minimum logging level
    )

logging.info("this is info") # prints 2017-05-11 17:36:33,141 INFO:this is info
```

Be careful with the logging level, the minimum logging level matters, as messages with lower level than the minimum will not be displayed or saved.

``` python
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)        # minimum logging level

logging.debug("this is debug") # won't be displayed because DEBUG < INFO
```

### Generators

A generator produces a sequence of results and avoid loading an iterable object all at once. For instance we never load a full array in memory, instead we load and process its element one by one by calling the `next()` method.

``` python
def yrange(n):
    i = 0
    while i < n:    # the loop doesn't run all at once, it waits for next()
        yield i
        i += 1

y = yrange(3)       # generator object
print y.next()      # prints 0
print y.next()      # prints 1
print y.next()      # prints 2
print y.next()      # raises Error
```

## Structure of a project

In this section we wil learn about modules, and how to organise a project that has multiple classes or functions declared in separated files.

### Importance of an `__init__.py` file

Adding a `__init__.py` file within a folder makes the folder a python module, that can be imported in other python files. Let's say we defined a function `some_function` within the `my_module.__init__.py` file. This function is now part of a module called `my_module`.

``` bash
my_python_project/
├── __init__.py
└── my_module
    └── __init__.py
```

Within `my_python_project.__init__.py`, we write:

``` python
from my_module import some_function

def main():
    some_function()

if __name__ == "__main__":
    main()
```

And in `my_python_project.my_module.__init__.py` we might have:

``` python
def some_function():
    return "hi"
```

## Sublime Text

I personally use Sublime Text 3 when writing python code for production. I like that it is lightweight and very extensible thanks to so many third parties packages. In the following, I share with you some of my favorite packages.

### Install Sublime Text 3 & Package Control

1. Download from [here](https://www.sublimetext.com/3)

2. Install Package Control from [here](https://packagecontrol.io/installation).
Package control will enable you to browse and install awesome packages to make
Sublime Text even better.

3. Launch Package Control from Sublime Text with `CTRL` + `MAJ` + `P` and
search for Package Control. Autocomplete should bring you a list of various commands.

### My Favorite Packages

1. [SideBarEnhancements](https://packagecontrol.io/packages/SideBarEnhancements),
adds tons of options to the Sublime Text sidebar.
2. [GitGutter](https://packagecontrol.io/packages/GitGutter): See git diff in Sublime Text
3. [BracketHighlighter](https://packagecontrol.io/packages/BracketHighlighter): Bracket and tag highlighter for Sublime Text
4. [All Autocomplete](https://packagecontrol.io/packages/All%20Autocomplete): Extend Sublime Text autocompletion to find matches
in all open files.
5. [Markdown Preview](https://packagecontrol.io/packages/Markdown%20Preview): Write markdown and then render as HTML
6. [SublimeCodeIntel](https://packagecontrol.io/packages/SublimeCodeIntel): Smart autocompletion for Sublime Text
7. [Agila Theme](https://packagecontrol.io/packages/Agila%20Theme): One theme among others

## Vim

I recently switched from Sublime Text to Vim even though I don't master all the commands available. I was inspired by my coworker at ManoMano [Francois](https://choiz.fr) who taught me a lot about Vim, what configuration I should have, and which plugins I should install. I forked his configuration [repository](https://github.com/ChoiZ/Micro-Vim-config) and added my own plugins and preferences. You can find my repository [here](https://github.com/ericdaat/Micro-Vim-Config).

## Virtual Environments

### What is it ?

From [virtualenv documentation](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/):
> A Virtual Environment is a tool to keep the dependencies required by different projects in separate places, by creating virtual Python environments for them. It solves the “Project X depends on version 1.x but, Project Y needs 4.x” dilemma, and keeps your global site-packages directory clean and manageable.

You should never **sudo** pip install something:

``` bash
sudo pip install whatever                     # bad
```

Instead, pip install any library you want **inside** a virtualenv:

``` bash
(your-virtualenv) pip install whatever        # good
```

### Getting started

Install virtualenv with pip

``` bash
pip install virtualenv  # you may need sudo
```

Create a virtualenv somewhere in your file system:

``` bash
virtualenv your-virtualenv  # will create a your-virtualenv folder
```

Activate it:

``` bash
source your-virtualenv/bin/activate
(your-virtualenv) pip list # check what's inside
```

You're free ! Install whatever you want !

``` bash
(your-virtualenv) pip install pandas
```

### It gets better

You can use whatever python you want !

```shell
virtualenv your-virtualenv -p python3
```

Export all you pip libraries to a .txt file:

```shell
(your-virtualenv) pip freeze > requirements.txt
```

Install back your pip libraries in another virtualenv:

```shell
(your-virtualenv2) pip install -r requirements.txt
```

## Writing Beautiful Python

### PEP 8

A guide written by Guido van Rossum, Barray Warsaw and Nick Coghlan for defining naming and formatting conventions accross all python scripts.

Taken from [python.org](https://www.python.org/dev/peps/pep-0008/):

* [Code layout](https://www.python.org/dev/peps/pep-0008/#code-lay-out)
* [Naming conventions](https://www.python.org/dev/peps/pep-0008/#naming-conventions)

## Thank you

That's it ! I hope this post made sense and helped you a little ! Have fun progamming in this beautiful language that is Python.

<iframe src="https://giphy.com/embed/ZVik7pBtu9dNS" width="480" height="268" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/life-interesting-footage-ZVik7pBtu9dNS">via GIPHY</a></p>
