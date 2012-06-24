from collective.behavior.stock import _
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import Int


class IStock(Interface):
    """Interface for Stock behavior."""

    unlimited = Bool(
        title=_(u"Unlimited Stock"),
        description=_(u"Check if you do not need to worry about stock ie practically unlimited stock."))

    stock = Int(
        title=_(u'Stock'),
        default=0,
        min=0)

    reducible_quantity = Int(
        title=_(u'Maximum Reducible Quantity'),
        description=_(u'This amount is the maximum limit quantity to reduce the stock at once. Keep this 0 if you do not need to set the limit.'),
        default=0,
        min=0)
