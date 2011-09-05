# -*- coding: utf-8 -*-

from five import grok

from plone.directives import form, dexterity


class IProject(form.Schema):
    pass


class View(grok.View):
    grok.context(IProject)
    grok.require('zope2.View')
