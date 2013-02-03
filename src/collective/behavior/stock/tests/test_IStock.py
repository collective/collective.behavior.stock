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
            schema.description, u'The maximum quantity to be reduced at once.')

    def test_reducible_quantity__default(self):
        schema = self.get_schema('reducible_quantity')
        self.assertEqual(
            schema.default, 100)

    def test_reducible_quantity__min(self):
        schema = self.get_schema('reducible_quantity')
        self.assertEqual(
            schema.min, 1)
