from collective.behavior.stock import _
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import Attribute


class IStock(Schema):
    """Interface for Stock behavior."""

    reducible_quantity = schema.Int(
        title=_(u'Maximum Reducible Quantity'),
        description=_(u'The maximum quantity to be reduced at once.'),
        default=100,
        min=1)

    initial_stock = Attribute('Sum of initial stocks')
    stock = Attribute('Sum of stocks')

    def stocks(sort_order='ascending'):  # pragma: no cover
        """Returns catalog brains of stock."""

    def sub_stock(value):  # pragma: no cover
        """Decrease stock by value and return the real subtracted value."""

    def add_stock(value):  # pragma: no cover
        """Add stock by value and return the real added value."""
