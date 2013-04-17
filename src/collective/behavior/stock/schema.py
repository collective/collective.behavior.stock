from collective.behavior.stock import _
from plone.supermodel.model import Schema
from zope import schema


class StockSchema(Schema):
    """Schema for behavior: Stock"""

    reducible_quantity = schema.Int(
        title=_(u'Maximum Reducible Quantity'),
        description=_(u'The maximum quantity to be reduced at once.'),
        default=100,
        min=1)
