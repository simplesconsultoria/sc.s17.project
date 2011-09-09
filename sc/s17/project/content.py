# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from five import grok

from plone.directives import form


class IProject(form.Schema):
    pass


class View(grok.View):
    grok.context(IProject)
    grok.require('zope2.View')

    def contents(self):
        """Return a catalog search result of project's contents.
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        contents = catalog(path='/'.join(context.getPhysicalPath()),
                           sort_on='getObjPositionInParent')

        return contents
