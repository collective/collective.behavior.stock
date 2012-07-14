from collective.behavior.stock import _
from zope.interface import Interface
from zope.schema import Int


class IStock(Interface):
    """Interface for Stock behavior."""

    reducible_quantity = Int(
        title=_(u'Maximum Reducible Quantity'),
        description=_(u'The maximum quantity to be reduced at once.'),
        default=100,
        min=1)
