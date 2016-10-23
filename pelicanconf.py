#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Elliot Tucker'
SITENAME = u"Elliot's Stuff"
SITEURL = 'https://elliottucker.net'

TIMEZONE = 'Europe/Dublin'

DEFAULT_LANG = u'en'

THEME="pelican-themes/pelican-bootstrap3"
PYGMENTS_STYLE="monokai"
AVATAR="images/me.jpg"
PATH="content"
SITELOGO="images/me.jpg"
SITELOGO_SIZE="30px"
FAVICON="images/me.jpg"
HIDE_SITENAME=True



BOOTSTRAP_NAVBAR_INVERSE=True

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
# Blogroll
#LINKS =  (('Photos', 'http://elliottucker.net/bestof/'),)
#           ('Python.org', 'http://python.org/'),
#           ('Jinja2', 'http://jinja.pocoo.org/'),
#           ('You can modify those links in your config file', '#'),)

MENUITEMS = (("Photos","/photos/bestof"),)

# Social widget
SOCIAL = (('Twitter', 'http://twitter.com/elliottucker'),
          ('500px', 'http://www.500px.com/elliottucker'),
          ('Google+','https://plus.google.com/+ElliotTucker'),
          ('LinkedIn', 'https://ie.linkedin.com/in/elliottucker/')
          )



DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', '.well-known']
