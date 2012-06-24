from collective.behavior.stock.interfaces import IStock
from plone.directives import form
from rwproperty import getproperty
from rwproperty import setproperty
from zope.interface import alsoProvides
from zope.interface import implements

import logging

logger = logging.getLogger(__name__)


alsoProvides(IStock, form.IFormFieldProvider)


class Stock(object):
    """
    """
    implements(IStock)

    def __init__(self, context):
        self.context = context

    @getproperty
    def unlimited(self):
        return getattr(self.context, 'unlimited', False)

    @setproperty
    def unlimited(self, value):
        """Set unlimited as Boolean

        :param value: True or False
        :type value: bool
        """
        if value is not True:
            if value is not False:
                raise ValueError('Not Bool')
        setattr(self.context, 'unlimited', value)

    @getproperty
    def stock(self):
        return getattr(self.context, 'stock', 0)

    @setproperty
    def stock(self, value):
        """Setting stock as Integer

        :param value: Stock value such as 10.
        :type value: int
        """
        if isinstance(value, int):
            # Set stock
            setattr(self.context, 'stock', value)
        else:
            raise ValueError('Not Integer')

    @getproperty
    def reducible_quantity(self):
        return getattr(self.context, 'reducible_quantity', 0)

    @setproperty
    def reducible_quantity(self, value):
        """Setting reducible_quantity as Integer

        :param value: Stock value such as 10.
        :type value: int
        """
        if isinstance(value, int):
            # Set reducible_quantity
            setattr(self.context, 'reducible_quantity', value)
        else:
            raise ValueError('Not Integer')
