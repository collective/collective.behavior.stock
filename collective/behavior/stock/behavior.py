from Products.CMFCore.utils import getToolByName
from collective.behavior.stock.interfaces import IStock
from collective.cart.stock.interfaces import IStock as IStockContent
from plone.directives import form
from zope.interface import alsoProvides
from zope.interface import implements
from zope.lifecycleevent import modified


alsoProvides(IStock, form.IFormFieldProvider)


class Stock(object):
    """
    """
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

    def _query(self, sort_order='ascending'):
        return {
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1,
            },
            'object_provides': IStockContent.__identifier__,
            'sort_on': 'created',
            'sort_order': sort_order,
        }

    @property
    def stock(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return sum([brain.stock for brain in catalog(self._query())])

    def sub_stock(self, value):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = [brain for brain in catalog(self._query()) if brain.stock > 0]
        if brains and sum([brain.stock for brain in brains]) >= value:
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
            return self.stock
        else:
            raise ValueError('Not possible to reduce more than zero.')

    def add_stock(self, value):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(self._query(sort_order='descending'))
        stock = sum([brain.stock for brain in brains])
        max_stock = sum([brain.initial_stock for brain in brains])
        if brains and value <= max_stock - stock:
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
            return self.stock
        else:
            message = 'Not possible to add more than max stock: {}.'.format(max_stock)
            raise ValueError(message)
