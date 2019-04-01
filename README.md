# Personal Tech Blog

This blog is hosted with Github Pages, on
[ericdaat.github.io](https://ericdaat.github.io).

It is built with [Pelican](https://blog.getpelican.com/),
a static site generator writen in Python.

## Installation

Install requirements in virtualenv:

``` text
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements
```

Install the theme:

``` text
pelican-themes --install themes/aboutwilson
```

## Commands

- Write HTML files: `make html`
- Serve on localhost: `make serve`
- Publish to github: `make publish github`
