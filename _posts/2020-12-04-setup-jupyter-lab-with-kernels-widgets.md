---
layout: post
title: Setup Jupyter Lab with Kernels and Widgets
date: 2020-12-04
last_modified_at: 2020-12-04
excerpt:
  Jupyter Lab is a very useful tool to write Python code. I use it all the
  time when I'm starting a new project. It's also a good way to present
  something you're working on and add notes next to your code.
  This post will help you setup Jupyter Lab with various kernels and
  widgets, so that your productivity increases.
cover: jupyterlab.png
image: /assets/img/eric.jpg
categories: ["Computer Setup", "Software Engineering"]
---

We are going to see how to make it from
[Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/) most basic interface
to a more sophisticated one, with kernels, widgets and everything to make
you love Jupyter Lab even more. You will start from the picture on the left,
and hopefully end up with the picture on the right.

<div class="container">
  <div class="row">

    <div class="col">
      <img src="/assets/img/articles/jupyterlab/jupyter_1.png" width="100%">
    </div>

    <div class="col">
      <img src="/assets/img/articles/jupyterlab/jupyter_10.png" width="100%">
    </div>

  </div>
</div>

## Setup

Install Jupyter Lab:

``` bash
pip3 instal jupyterlab
```

Launch it with:

``` bash
jupyter-lab
```

Note: I prefer to launch it in the background with tmux:

``` bash
tmux new -d -s jupyter "jupyter-lab --no-browser"
```

It's even cooler to use aliases, in your `.zshrc` (or `.bashrc` ), append:

``` bash
alias jupyter-tmux='tmux new -d -s jupyter "jupyter-lab --no-browser"';
alias tas='tmux attach-session -t'
```

Then launch jupyter with:

``` bash
jupyter-tmux
```

Attach to the session with:

``` bash
tas jupyter
```

## Install Kernels

Jupyter comes with a default [Python](https://www.python.org/) kernel,
the one installed on your computer. This is a good start but you might want
to use different python environments
(if you're used to working with `virtualenv` for instance) with different
python versions or librairies. You might also want to use Jupyter Lab with
other programming languages, like `R` or `Julia`. If that sounds appealing to
you, look no further, we are going to install kernels !

The installed kernels will be located under `$HOME/Library/Jupyter/kernels`.

### Python kernel from a virtual environment

Let's first add Python kernels to Jupyter Lab. I am going to assume you are
familiar with virtual environments, if not you should refer to this tutorial:
[Pipenv & Virtual Environments](https://docs.python-guide.org/dev/virtualenvs/).

Make sure you have `virtualenv` installed on your computer:

``` bash
pip3 install virtualenv
```

##### Step 1: A Python 3 Kernel

We are going to create a first kernel based on Python 3, and we are going to
name it "Python (data-science)". It's fairly easy:

- Create the virtual environment based on `python3`
  ``` bash
  virtualenv data-science -p python3
  ```
- Activate the environment
  ``` bash
  source data-science/bin/activate
  ```
- Install `ipykernel` within it
  ``` bash
  pip install ipykernel
  ```
- Register the environment as a kernel, give it a name and a display name
  ``` bash
  python -m ipykernel install --user --name data-science --display-name "Python (data-science)"
  ```

##### Step 2: A Python 2 Kernel

By following the same steps, here's how to add a Python 2 kernel, for your
legacy projects:

``` bash
virtualenv python2 -p python2
source data-science/bin/activate
pip install ipykernel
python -m ipykernel install --user --name python2 --display-name "Python 2"
```

Now if you install libraries within one of these virtual environments, they
will be available though the corresponding Jupyter Lab kernel.
If you reload your Jupyter Lab interface, you should see something like this:

<img src="/assets/img/articles/jupyterlab/jupyter_2.png" width="100%">

Here are some useful commands:

- List your kernels:
  ``` bash
  jupyter kernelspec list
  ```
- Uninstall a kernel:
  ``` bash
  jupyter kernelspec uninstall data-science
  ```

### Kernels with other programming languages

The nice thing about Jupyter Lab is that you're not limited to Python. Let's
see how to use other languages like [R](https://www.r-project.org/) and
[Julia](https://julialang.org/) within notebooks.

##### R Kernel

Assuming you have R installed, run these lines in a terminal:

``` bash
Rscript -e 'install.packages(c("repr", "IRdisplay", "IRkernel"), type = "source", repos="https://cran.rstudio.com");'
Rscript -e 'IRkernel::installspec()'
```

Reload Jupyter Lab and you should see this:

<img src="/assets/img/articles/jupyterlab/jupyter_3.png" width="100%">

Nice, R kernel just appeared. Here's another trick, you can actually write `R`
code within a `Python` notebook. For this, you need to install the library
`rpy2`:

``` bash
pip3 install rpy2
```

Then, from a Python notebook cell, load the `rpy2` extension:

``` python
%load_ext rpy2.ipython
```

You can now write R code within that cell! For instance:

<img src="/assets/img/articles/jupyterlab/jupyter_4.png" width="100%">

##### Julia kernel

I have been recently introduced to the Julia programming language, and it
seems very fun and powerful. Let's create a Julia kernel, because why not ?

Assuming you have Julia installed, launch Julia from a terminal
(just run `Julia`) and then type:

``` julia
Pkg.add("IJulia")
```

Reload Jupyter Lab as usual, and you should now see the new Julia kernel:

<img src="/assets/img/articles/jupyterlab/jupyter_5.png" width="100%">

That's pretty neat, we now have 5 kernels:

- Python 3: the default python on your computer
- Python (data-science): python 3 from a virtual environment
- Python 2: python 2 from a virtual environment
- R: to run R code
- Julia: to run Julia code

## Widgets

Let's now tweak our beloved Jupyter Lab by adding some widgets. Namely:

- [Table of contents](https://github.com/jupyterlab/jupyterlab-toc):
  automatically generate a table of contents for your
  notebook, based on the markdown sections you wrote
- [Git](https://github.com/jupyterlab/jupyterlab-git):
  If working within a git repository, directly add & commit from
  the Jupyter Lab interface
- [Latex](https://github.com/jupyterlab/jupyterlab-latex):
  Write and compile Latex files from Jupyter Lab
- [Templates](https://pypi.org/project/jupyterlab-templates/):
  Lets you start a notebook from a template

Note: you can either install extensions from the command line, or by using
the "Extension Manager" tab within the Jupyter Lab user interface. I
prefer the command line though, it's easier to store my extensions and
make a script to automatically install them.

### Table of contents

As mentioned earlier, this widget generates a table of content from your
notebook.

Install it with:

``` bash
jupyter-labextension install @jupyterlab/toc
```

You'll see a new tab appear, when you click on it, it'll show
the table of content. The sections are automatically created based on the
markdown sections. Note that you can either enable automatic numbering or not.
I did enable it on the following screenshot, and it looks like this:

<img src="/assets/img/articles/jupyterlab/jupyter_6.png" width="100%">

### Git

If you're tired of running back and forth between your terminal and Jupyter
Lab to commit your code, consider this extension that brings a Git interface
to Jupyter Lab. Install it with:

``` bash
pip3 install jupyterlab-git
jupyter-labextension install @jupyterlab/git
```

As usual, a new tab appears:

<img src="/assets/img/articles/jupyterlab/jupyter_7.png" width="100%">

### Latex

I mostly use overleaf for Latex, but if you're not and if you wish to use
Jupyter Lab for compiling Latex documents, this plugin will do the job.
Install it with:

``` bash
pip3 install jupyterlab_latex
jupyter-labextension install @jupyterlab/latex
```

Now when you are editing a Latex file, a right click on the document will
show an option that lets you render the file to pdf:

<img src="/assets/img/articles/jupyterlab/jupyter_8.png" width="100%">

### Templates

Sometimes you might feel like you always copy paste the same lines of code
at the beginning of a new notebook. If you are, consider using notebook
templates with this plugin. Install it with:

``` bash
pip3 install jupyterlab_templates
jupyter labextension install jupyterlab_templates
jupyter serverextension enable --py jupyterlab_templates
```

Then you will see a new "Template" icon next to your kernels. If you click on
it, you will be asked which template you want to use, and it will create
a notebook based on this template. You can create your own templates by
saving notebooks in the template directory. You also get to choose which
directory the plugin will pick the templates from.

<img src="/assets/img/articles/jupyterlab/jupyter_9.png" width="100%">

## Wrapping up

You know now how to setup Jupyter Lab and enhance it with kernels and widgets.
There's a lot more to it and I'd love to hear about what kernels and widgets
you love. Feel free to reach out in the comments. I hope this tutorial was
somehow helpful.
