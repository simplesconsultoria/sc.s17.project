from five import grok
from zope import schema

from plone.directives import form, dexterity

from sc.s17.project import MessageFactory as _

class IProject(form.Schema):
    
    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u""),
        )
    
    description = schema.Text(
            title=_(u"Description"),
            description=_(u""),
            required=False,
        )