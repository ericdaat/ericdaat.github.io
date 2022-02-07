---
layout: post
title: A minimal Flask application with Bootstrap assets
date: 2022-02-07
last_modified_at: 2022-02-07
excerpt:
  This tutorial is a starting point for everyone who wants to build a web
  application using Python Flask along with Bootstrap. Instead of importing
  Bootstrap from the CDN, I am installing it with npm and I use Sass to customize it.
cover: flask.jpg
image: /assets/img/eric.jpg
categories: ["Software Engineering"]
---

Flask is a lightweight framework used for developing web applications using
python. Flask aims to keep the core simple but extensible. For instance, it
does not come with an existing database abstraction layer like Django does and
you're free to choose what database to use.

As there are already many great tutorials on Flask, I am not going to cover
the basics here, and I will assume you're already familiar with it. However,
if you are not, feel free to check the following resources:

- [Flask website](https://flask.palletsprojects.com/en/2.0.x/)
- [Flask quickstart guide](https://flask.palletsprojects.com/en/2.0.x/quickstart/)
- [Flask tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/)
- [Flask deployment options](https://flask.palletsprojects.com/en/2.0.x/deploying/)

We use Flask to build our application backend and we will use Bootstrap for
front-end. Again, I am not going to cover how to use Bootstrap here,
and you can check the [Bootstrap official documentation](https://getbootstrap.com/) to learn more if you're not
familiar with it.

## Project Layout

All the code used in this tutorial is available in the following Github
repository: [github.com/ericdaat/flask-assets-bootstrap](https://github.com/ericdaat/flask-assets-bootstrap).

The application code is located in the [application](https://github.com/ericdaat/flask-assets-bootstrap/tree/main/application)
directory, and is organized as such:

```text
application
├── __init__.py
├── app.py                 --> Flask app code and routes
├── static                 --> Static files
│ ├── assets
│ │ ├── main.scss          --> Main stylesheet, will import Bootstrap and customize it
│ │ ├── node_modules       --> Modules such as Bootstrap will be installed here
│ │ ├── package-lock.json
│ │ └── package.json
│ ├── css
│ │ └── scss-generated.css --> Generated CSS file (from main.scss)
│ └── js
│     └── generated.js     --> Generated JS file
└── templates              --> HTML template files
    ├── base.html          --> Base template
    └── index.html         --> Template returned by the application
```

We will cover most files individually in the following sections to explain what
is going on.

## A basic Flask application

Let's start by creating a very basic web application, with a single route,
that renders a simple HTML template. This corresponds to the `app.py` file.

``` python
from flask import Flask, render_template

# create app
app = Flask(__name__)

# app routes
@app.route("/")
def index():
    return render_template("index.html")
```

The HTML template file is very simple and uses a Bootstrap container,
with some top margin. This file is located in `templates/index.html`.
This template inherits from `templates/base.html`, but we will get to this later.

{% raw %}
``` html
{% extends "base.html" %}

<div class="container mt-5">
    <h1>A Flask application with Bootstrap Sass</h1>

    <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    </p>
</div>
```
{% endraw %}

So far, if you try to run the application, no styling will be applied as
Bootstrap is not installed yet. Let's fix that.

## Installing Bootstrap

There are multiple ways to install Bootstrap, as detailed in the
[official documentation](https://getbootstrap.com/docs/5.1/getting-started/introduction/).
In this tutorial, we will use [npm](https://www.npmjs.com/) to install bootstrap,
and the installation folder will be located in `static/assets/node_modules`.

``` bash
mkdir -p static/assets;
cd static/assets;
npm init;
npm install bootstrap;
cd -;
```

We are going to use [Sass](https://sass-lang.com/) along with Bootstrap to
style our application. [Sass](https://sass-lang.com/) is a very popular CSS
extension language that adds many features,
as shown in [this tutorial](https://sass-lang.com/guide). Bootstrap can be
imported and customized in Sass, as explained in the
[Bootstrap documentation](https://getbootstrap.com/docs/5.1/customize/sass/).

Let's create a `main.scss` file under `static/assets/`, that looks like this:

``` javascript
// static/assets/main.scss
// Source: https://getbootstrap.com/docs/5.1/customize/sass/#importing

// Custom Bootstrap variables
$body-bg: black;    // body background is black
$body-color: white; // body text is white

// Include all of Bootstrap
@import "node_modules/bootstrap/scss/bootstrap";
```

## Using Flask-Assets to read the SCSS file

Bootstrap is now installed and customized, but Flask does not know it yet.
To fix this, we are going to need the [Flask-Assets](https://flask-assets.readthedocs.io/en/latest/)
extension. We are also going to need `libsass`. Let's install both via `pip`.

``` bash
pip install Flask-Assets libsass;
```

Let's edit our `app.py` file, and add the following lines:

First, we initialize the app by creating an Environment instance.

``` python
# https://flask-assets.readthedocs.io/en/latest/#usage
assets = Environment(app)
assets.url = app.static_url_path
```

Then, we register our `main.scss` asset using a Bundle. The following
lines of code will:

1. Read the `main.scss` file and generate a css file based on it, using the
   libsass filter.
2. Output the generated .css file in the `static/css` folder. We chose to name
   it `scss-generated.css`.
3. Register the generated css file, to be used in Jinja templates

``` python
# Scss files
scss = Bundle(
    "assets/main.scss",  # 1. will read this scss file and generate a css file based on it
    filters="libsass",   # using this filter: https://webassets.readthedocs.io/en/latest/builtin_filters.html#libsass
    output="css/scss-generated.css"  # 2. and output the generated .css file in the static/css folder
)
assets.register("scss_all", scss)  # 3. register the generated css file, to be used in Jinja templates (see base.html)
```

Now the last step is to include the generated CSS file in our Flask template.
To do so, we add the following lines to our `templates/base.html` file.
The `ASSET_URL` variable points to the generated CSS path. Flask knows
this because we used the same name `scss_all` when registering the bundle
and when calling `% assets "scss_all" %` in the HTML file.

{% raw %}
``` html
<!-- https://flask-assets.readthedocs.io/en/latest/#using-the-bundles -->
{% assets "scss_all" %}
    <link rel=stylesheet type=text/css href="{{ ASSET_URL }}">
{% endassets %}
```
{% endraw %}

## Using Flask-Assets with Javascript

Flask-Assets can also be used to parse Javascript files required by Bootstrap.
This works very similarly to what we did earlier.

First, let's install jquery, required by Bootstrap:

``` bash
npm install jquery
```

Then, edit the `app.py` file and add a Javascript bundle:

``` python
# JS files
js = Bundle(
    "assets/node_modules/jquery/dist/jquery.min.js",
    "assets/node_modules/@popperjs/core/dist/umd/popper.min.js",
    "assets/node_modules/bootstrap/dist/js/bootstrap.min.js",
    filters="jsmin",
    output="js/generated.js"
)
assets.register("js_all", js)
```

This Bundle will:
- Read the three JS scripts `jquery.min.js`, `popper.min.js` and
`bootstrap.min.js`
- Combine them into a `js/generated.js` file, that we can load in Flask.

Finally, edit the `templates/base.html` file and add these lines:

{% raw %}
``` html
{% assets "js_all" %}
  <script type="text/javascript" src="{{ ASSET_URL }}"></script>
{% endassets %}
```
{% endraw %}

## Using my template repository

Feel free to clone my template repository
[github.com/ericdaat/flask-assets-bootstrap](https://github.com/ericdaat/flask-assets-bootstrap)
and extend it with your code. The project layout is the same as in this
tutorial, and the app is very basic so that it is easy to start with.

I hope this post was useful, please feel free to suggest improvements or report
bugs.
