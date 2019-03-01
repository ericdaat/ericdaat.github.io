#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Eric Daoud'
SITEURL = ''
SITENAME = 'Eric\'s Blog'
SITETITLE = 'Eric\'s Blog'
SITESUBTITLE = 'Data Scientist, Full Stack Developer'
SITEDESCRIPTION = 'Yet another tech blog where I talk about what I do and like.'
SITELOGO = '/images/eric.jpg'
FAVICON = '/images/favicon.ico'
TIMEZONE = "Europe/Paris"

PATH = 'content'
STATIC_PATHS = ['images', 'extra']

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

MAIN_MENU = True

MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'))

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (('Github', 'https://github.com/ericdaat'),
          ('Twitter', 'https://twitter.com/ericdaoud'),
          ('Youtube', 'https://www.youtube.com/user/ericmusic13'),
          ('Linkedin', 'https://www.linkedin.com/in/ericdaoud/'),
          ('500px', 'https://500px.com/ericda'),)

DEFAULT_PAGINATION = 10

MARKUP = ('md', 'ipynb')

DEFAULT_METADATA = {
    'status': 'draft',
}

EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

# Plugins
PLUGIN_PATHS = ['./plugins']
PLUGINS = ['render_math', 'pelican_gist',]

# Themes
THEME = 'aboutwilson'

# code blocks with line numbers
# PYGMENTS_MD_OPTIONS = {'linenos': 'table'}
# PYGMENTS_STYLE = 'monokai'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

SLUGIFY_SOURCE = 'title'