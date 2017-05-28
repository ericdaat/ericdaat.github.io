Title: Python Tips and Tools
Date: 2017-05-28 10:20
Modified: 2017-05-28 10:20
Category: Programming
Tags: python, code
Slug: python-tips-and-tools
Authors: Eric Daoud
Summary: Showing some tips and useful stuff I like about Python language.
Status: published


I love Python programming language, and I have been using it for several years now. It is a very simple yet powerful language that is used for so many purposes. It is quite an old language created by Guido Van Rossum in 1989 ... because he was bored ! 

> *Over six years ago, in December 1989, I was looking for a "hobby" programming project that would keep me occupied during the week around Christmas. My office ... would be closed, but I had a home computer, and not much else on my hands. I decided to write an interpreter for the new scripting language I had been thinking about lately: a descendant of ABC that would appeal to Unix/C hackers. I chose Python as a working title for the project, being in a slightly irreverent mood (and a big fan of Monty Python's Flying Circus).*  

> -- Guido Van Rossum, 1996

There are a few Python things I learnt over the years, and I decided to share them in this post. I'll cover the basis of Object Oriented Programming; then some useful functions or tools that I like about the language; finally, I'll speak about how to organise a project and install libraries with virtual environments. 

Before we dive in this article, let me mention a few things:

1. This is absolutely not exhaustive. I am very aware that I don't know all about Python and have no legitimacy teaching it. I just wanted to share some of my favorite aspects of the language.
2. You can learn more about Python [here](https://www.python.org/).
3. I personally started learning it by reading [Learn Python the Hard Way](https://learnpythonthehardway.org/book/)
4. For Mac users, it is recommended to **not** use the built in macOS Python. Instead, do the following:
    - Get [Homebrew](https://brew.sh/), the missing package manager for macOS
    - Run ``` brew install python```

## Object Oriented Programming

A python code doesn't need to be Object Oriented, as opposed to Java for instance: It can be used as a scripting language. However in many projects you will need classes and methods. This section will explain how to write Object Oriented code in Python. Note that this assumes that you know of Object Oriented Programming, I am not going to explain the theory behind it. If you are not familiar with it, I recommended checking out this [Wikipedia](https://en.wikipedia.org/wiki/Object-oriented_programming) post.

### Simple Class

We create a basic class `MyClass` with a constructor `__init__` that takes no argument. Our class is very simple and has no attribute.

``` python
class MyClass(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    my_class = MyClass()    # call to the __init__ constructor
```

### Passing arguments

Let's improve our class by changing the constructor and adding arguments.

``` python
class MyClass(object):
    def __init__(self, arg):
        self.arg = arg

if __name__ == '__main__':
    my_class = MyClass(1)   # call to the __init__ constructor
    print my_class.arg      # will print 1
```

Note that unlike Java, you can't define multiple constructors for one same class.

``` python
class MyClass(object):
    def __init__(self, arg):
        self.arg = arg

    def __init__(self): # this will not work, since we already defined a constructor
        self.arg = 1
```

### Calling methods

We can now add an instance method to our class. Such a method must always have `self` as first argument. It is a reference to the object itself.

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

Create two Classes `A` and `B`, where `B` inherits from `A`. Notice
how `B` can use `a_method` even though it is defined in `A`.

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

## Overidding

Same `A` and `B` Classes, but this time we override
`A.a_method` in `B`

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

## instance method vs. Class method

An instance method is called on an instance of the Class.  
Here, `Animal` is our class, and `bob` is an instance of `Animal`.

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

## Public vs. private

Methods and attributes are public by default in python. Adding a `_` makes
them private:

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

## Accessing private attributes: getter & setter

When defining private attributes, we can access them with getters,
and redefine them with setters.


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

# Useful tools and functions
## Comprehension lists

Creating arrays faster and in a more elegant way.

``` python
# The ugly way:
l = []
for i in range(5):
    l.append(i)
# l = [0, 1, 2, 3, 4]


# The list comprehension way:
l = [i for i in range(5)]
# l = [0, 1, 2, 3, 4]


# Works with dicts too !
d = {str(i):i for i in range(5)}
# d = {'1': 1, '0': 0, '3': 3, '2': 2, '4': 4}

```

## Enumerate

An elegant way to iterate over an iterable object

``` python
l = [10, 20, 30]

# The ugly way:
for i in range(len(l)):
    print i, l[i]               # will print 0, 10 then 1, 20 etc ...


# The enumerate way:
for i, item in enumerate(l):    # enumerate(l) = [(0, 10), ...]
    print i, item               # print the same thing, but nicer !
```

## Map functions

Apply a function to every item of an iterable object (e.g. arrays).

``` python
l = [1, 2, 3]           # l is an iterable object

def f(value):           # function to apply to l items
    return 2 * value


# The ugly way:
new_l = []
for i in range(len(l)):
    new_l.append(f(l))
# new_l = [2, 4, 6]


# The map way:
new_l = map(f, l)
# new_l = [2, 4, 6]

```

## Lambda functions

Create anonymous functions.

``` python
l = [1, 2, 3]

def f(value):
    return 2 * value

print map(f, l) 
```

Do we really need to declare a function for such an easy operation ? Nope.

``` python
l = [1, 2, 3]

print map(lambda r: r*2, l)     # will print [2, 4, 6]
```

## Partial functions

Functions used in map can only take a single argument. What if we have more ?
Here, we learn to create a partial function filled with some constant 
arguments and leave one free, so we can map values on it.

``` python
from functools import partial

l = [1,2,3]

def f(value, coefficient):          # would be hard to map huh ?
    return value * coefficient

fp = partial(f, coefficient=2)      # fp = f(value, coefficient=2)

print map(fp, l)                    # will print [2, 4, 6]

```

## Multiprocessing with Pool

Multi process a function with multiprocessing.Pool

``` python
from multiprocessing import Pool
import time

def f(value):
    time.sleep(1)
    return value

l = [1, 2, 3, 4]
p = Pool(4)         # say we have 4 cores --> 4 processes

map(f, l)           # would take 4 seconds
p.map(f, l)         # would take 1 second

```

## Handling Exceptions: with try & except

Things will break.

``` python
l = [1, 2, 3, None]

for i, item in enumerate(l):
    print l + 1     # will crash when item=None
```

Handle exceptions:

``` python
l = [1, 2, 3, None]

for i, item in enumerate(l):
    try:
        print l + 1
    except:     # Will catch any exception (KeyError, ValueError, etc...)
        print "Something went wrong"
```

Full list of Exceptions [here](https://docs.python.org/2/library/exceptions.html#bltin-exceptions).

## Assertions

Checks boolean expressions, raises exception when False.

``` python
assert(2>=1)     # works
assert(2<=1)     # raises AssertionError
```

Useful for parameter checking:
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

## Loop statements
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

## Logging

Are you using `print` for logging ? Stop right now.

``` python
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG)     # minimum logging level

logging.info("this is info") # prints 2017-05-11 17:36:33,141 INFO:this is info
```

Be careful with the logging level.

``` python
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)        # minimum logging level

logging.debug("this is debug") # won't be displayed because DEBUG < INFO
```

## Generators

A generator produces a sequence of results and not the full array. Hence, we never load a full array in memory.

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

#Structure of a project

## `__init__.py`

This is where the main function starts

```python
def main():
    # main function
    pass

if __name__ == "__main__":
    # this is the entrypoint of the code
    main()
```

## Modules

Let's say we defined a function `some_function` within 
the `my_module.__init__.py` file. This function is now part
of a module beautifully called `my_module`.

``` shell
my_python_project/
├── __init__.py
└── my_module
    └── __init__.py
```

`my_python_project.__init__.py` : 
``` python
from my_module import some_function

def main():
    some_function()

if __name__ == "__main__":
    main()
```

# For a better Sublime Text
## Install Sublime Text 3 & Package Control

Sublime Text is a text editor that can be enhanced with 
several packages.

1. Download from [here](https://www.sublimetext.com/3)  

2. Install Package Control from [here](https://packagecontrol.io/installation).
Package control will enable you to browse and install awesome packages to make
Sublime Text even better.  

3. Launch Package Control from Sublime Text with `CTRL` + `MAJ` + `P` and
search for Package Control. Autocomplete should bring you a list of various commands.
# For a better Sublime Text
## My Favorite Packages

1. [SideBarEnhancements](https://packagecontrol.io/packages/SideBarEnhancements),
adds tons of options to the Sublime Text sidebar.
2. [GitGutter](https://packagecontrol.io/packages/GitGutter): See git diff in Sublime Text
3. [BracketHighlighter](https://packagecontrol.io/packages/BracketHighlighter): Bracket and tag highlighter for Sublime Text
4. [All Autocomplete](https://packagecontrol.io/packages/All%20Autocomplete): Extend Sublime Text autocompletion to find matches 
in all open files.
5. [Markdown Preview](https://packagecontrol.io/packages/Markdown%20Preview): Write markdown and then render as HTML
6. [SublimeCodeIntel](https://packagecontrol.io/packages/SublimeCodeIntel): Smart autocompletion for Sublime Text
7. [Agila Theme](https://packagecontrol.io/packages/Agila%20Theme): One theme among others

# Virtual Environments
## What is it ?

From [virtualenv documentation](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/):
> A Virtual Environment is a tool to keep the dependencies required by different projects in separate places, by creating virtual Python environments for them. It solves the “Project X depends on version 1.x but, Project Y needs 4.x” dilemma, and keeps your global site-packages directory clean and manageable.

You should never **sudo** pip install something:
``` console
$ sudo pip install whatever                     # bad
```

Instead, pip install any library you want **inside** a virtualenv:
``` console
$ (your-virtualenv) pip install whatever        # good
``

## Getting started

Install virtualenv with pip
``` shell
$ pip install virtualenv  # you may need sudo
```

Create a virtualenv somewhere in your file system:
``` shell
$ virtualenv your-virtualenv  # will create a your-virtualenv folder
```

Activate it:
``` shell
$ source your-virtualenv/bin/activate
$ (your-virtualenv) pip list # check what's inside
```

You're free ! Install whatever you want !
``` shell
$ (your-virtualenv) pip install pandas
```

## It gets better

You can use whatever python you want !
```shell
$ virtualenv your-virtualenv -p python3
```

Export all you pip libraries to a .txt file:
```shell
$ (your-virtualenv) pip freeze > requirements.txt
```

Install back your pip libraries in another virtualenv:
```shell
$ (your-virtualenv2) pip install requirements.txt
```

# Writing Beautiful Python
## PEP 8

A guide written by Guido van Rossum, Barray Warsaw and Nick Coghlan for defining naming and formatting conventions accross all python scripts.

Taken from [python.org](https://www.python.org/dev/peps/pep-0008/):
- [Code layout](https://www.python.org/dev/peps/pep-0008/#code-lay-out)
- [Naming conventions](https://www.python.org/dev/peps/pep-0008/#naming-conventions)
