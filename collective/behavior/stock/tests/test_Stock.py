import mock
import unittest

StockInt = mock.Mock()


class TestStock(unittest.TestCase):

    def test_subclass(self):
        from collective.behavior.stock.behavior import Stock
        self.assertTrue(issubclass(Stock, object))

    @mock.patch('collective.behavior.stock.behavior.StockInt', StockInt)
    def create_instance(self, context=mock.Mock()):
        from collective.behavior.stock.behavior import Stock
        return Stock(context)

    def test_instance(self):
        instance = self.create_instance()
        from collective.behavior.stock.behavior import Stock
        self.assertIsInstance(instance, Stock)

    def test_instance_provides_IStock(self):
        instance = self.create_instance()
        from collective.behavior.stock.interfaces import IStock
        self.assertTrue(IStock.providedBy(instance))

    def test_instance__verifyObject(self):
        instance = self.create_instance()
        from collective.behavior.stock.interfaces import IStock
        from zope.interface.verify import verifyObject
        self.assertTrue(verifyObject(IStock, instance))

    def test_instance__context(self):
        context = mock.Mock()
        instance = self.create_instance(context=context)
        self.assertEqual(instance.context, context)

    def test_instance__stock(self):
        instance = self.create_instance()
        self.assertEqual(instance.stock, StockInt())

    def test_instance__reducible_quantity_empty(self):
        """First time access to reducible_quantity"""
        context = object()
        instance = self.create_instance(context=context)
        self.assertEqual(instance.reducible_quantity, 0)

    def set_reducible_quantity(self, instance, reducible_quantity):
        """Setting reducible_quantity to instance."""
        instance.reducible_quantity = reducible_quantity

    def test_instance__reducible_quantity__ValueError(self):
        """Raise ValueError when setting other than integer."""
        instance = self.create_instance()
        self.assertRaises(ValueError, lambda: self.set_reducible_quantity(instance, 'AAA'))

    def test_instance__reducible_quantity__set(self):
        instance = self.create_instance()
        reducible_quantity = 5
        instance.reducible_quantity = reducible_quantity
        self.assertEqual(instance.context.reducible_quantity, reducible_quantity)
