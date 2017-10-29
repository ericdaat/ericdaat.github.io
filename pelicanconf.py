#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Eric Daoud'
SITEURL = ''
SITENAME = 'Eric\'s Blog'
SITETITLE = 'Eric\'s Blog'
SITESUBTITLE = 'Jr. Data Scientist'
SITEDESCRIPTION = 'Foo Bar\'s Thoughts and Writings'
SITELOGO = '/images/eric.jpg'
# FAVICON = SITEURL + '/images/favicon.ico'
GOOGLE_ANALYTICS = 'UA-105599779-1'

PATH = 'content'
STATIC_PATHS = ['images']

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

# Plugins
PLUGIN_PATHS = ['./plugins']
PLUGINS = ['render_math']

# Themes
THEME = 'aboutwilson'

# code blocks with line numbers
# PYGMENTS_MD_OPTIONS = {'linenos': 'table'}
# PYGMENTS_STYLE = 'monokai'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
