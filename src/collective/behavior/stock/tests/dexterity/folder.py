from five import grok
from plone.directives import form


class ICFolder(form.Schema):
    """Generic container content type for versatile content."""


class View(grok.View):
    """Default view for page."""

    grok.context(ICFolder)
    grok.require('zope2.View')
    grok.name('view')
