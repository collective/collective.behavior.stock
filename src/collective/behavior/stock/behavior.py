from Products.CMFCore.utils import getToolByName
from collective.behavior.stock.interfaces import IStock
from collective.cart.stock.interfaces import IStock as IStockContent
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from zope.interface import implements
from zope.lifecycleevent import modified


alsoProvides(IStock, IFormFieldProvider)


class Stock(object):
    """Behavior to add stock field to content types"""

    implements(IStock)

    def __init__(self, context):
        self.context = context

    @property
    def reducible_quantity(self):
        return getattr(self.context, 'reducible_quantity', 0)

    @reducible_quantity.setter
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

    def stocks(self, sort_order='ascending'):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1,
            },
            'object_provides': IStockContent.__identifier__,
            'sort_on': 'getObjPositionInParent',
            'sort_order': sort_order,
        }

        return catalog(query)

    def initial_stock(self):
        return sum([brain.initial_stock for brain in self.stocks()])

    def stock(self):
        return sum([brain.stock for brain in self.stocks()])

    def sub_stock(self, value):
        brains = [brain for brain in self.stocks() if brain.stock > 0]
        total = value
        if value > self.stock():
            total = self.stock()
        value = total
        for brain in brains:
            obj = brain.getObject()
            if obj.stock >= value:
                obj.stock -= value
                modified(obj)
                break
            else:
                value -= obj.stock
                obj.stock = 0
                modified(obj)
        return total

    def add_stock(self, value):
        brains = self.stocks(sort_order='descending')
        total = value
        if total >= self.initial_stock() - self.stock():
            total = self.initial_stock() - self.stock()
        value = total
        if len(brains) > 1:
            if brains[0].created < brains[1].created:
                brains = reversed([brain for brain in brains])
        for brain in brains:
            obj = brain.getObject()
            if obj.initial_stock - obj.stock >= value:
                obj.stock += value
                modified(obj)
                break
            else:
                value -= (obj.initial_stock - obj.stock)
                obj.stock = obj.initial_stock
                modified(obj)
        return total
