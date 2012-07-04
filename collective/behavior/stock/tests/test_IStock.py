import unittest


class TestIStock(unittest.TestCase):

    def test_subclass(self):
        from collective.behavior.stock.interfaces import IStock
        from zope.interface import Interface
        self.assertTrue(issubclass(IStock, Interface))

    def get_schema(self, name):
        """Get schema by name.

        :param name: Name of schema.
        :type name: str
        """
        from collective.behavior.stock.interfaces import IStock
        return IStock.get(name)

    def test_unlimited__instance(self):
        schema = self.get_schema('unlimited')
        from zope.schema import Bool
        self.assertIsInstance(schema, Bool)

    def test_unlimited__title(self):
        schema = self.get_schema('unlimited')
        self.assertEqual(schema.title, u'Unlimited Stock')

    def test_unlimited__description(self):
        schema = self.get_schema('unlimited')
        self.assertEqual(
            schema.description, u'Check if you do not need to worry about stock ie practically unlimited stock.')

    def test_unlimited__default(self):
        schema = self.get_schema('unlimited')
        self.assertFalse(schema.default)

    def test_stock__instance(self):
        schema = self.get_schema('stock')
        from zope.schema import Int
        self.assertIsInstance(schema, Int)

    def test_stock__title(self):
        schema = self.get_schema('stock')
        self.assertEqual(schema.title, u'Stock')

    def test_stock__default(self):
        schema = self.get_schema('stock')
        self.assertEqual(
            schema.default, 0)

    def test_stock__min(self):
        schema = self.get_schema('stock')
        self.assertEqual(
            schema.min, 0)

    def test_reducible_quantity__instance(self):
        schema = self.get_schema('reducible_quantity')
        from zope.schema import Int
        self.assertIsInstance(schema, Int)

    def test_reducible_quantity__title(self):
        schema = self.get_schema('reducible_quantity')
        self.assertEqual(schema.title, u'Maximum Reducible Quantity')

    def test_reducible_quantity__description(self):
        schema = self.get_schema('reducible_quantity')
        self.assertEqual(
            schema.description, u'This amount is the maximum limit quantity to reduce the stock at once.')

    def test_reducible_quantity__default(self):
        schema = self.get_schema('reducible_quantity')
        self.assertEqual(
            schema.default, 100)

    def test_reducible_quantity__min(self):
        schema = self.get_schema('reducible_quantity')
        self.assertEqual(
            schema.min, 1)
