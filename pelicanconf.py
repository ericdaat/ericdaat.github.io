#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Foo Bar'
SITEURL = ''
SITENAME = 'Foo Bar\'s Blog'
SITETITLE = 'Foo Bar'
SITESUBTITLE = 'Web Developer'
SITEDESCRIPTION = 'Foo Bar\'s Thoughts and Writings'
# SITELOGO = SITEURL + '/images/profile.png'
# FAVICON = SITEURL + '/images/favicon.ico'

PATH = 'content'
STATIC_PATHS = ['images']

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

MAIN_MENU = True

MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (
	('github', '#'),
	('twitter', '#'),
	('youtube', '#'),
	('linkedin', '#'),
	('500px', '#'),
	)

DEFAULT_PAGINATION = 10

MARKUP = ('md', 'ipynb')

# Plugins
PLUGIN_PATHS = ['./plugins']
PLUGINS = ['ipynb.markup', 'render_math']

# Themes
THEME = 'Flex'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
