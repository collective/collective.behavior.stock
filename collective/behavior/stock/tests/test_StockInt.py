# -*- coding: utf-8 -*-
from collective.behavior.stock.tests.base import IntegrationTestCase


class TestStockInt(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']

    def test_subclass(self):
        from collective.behavior.stock.behavior import StockInt
        self.assertTrue(issubclass(StockInt, int))

    def create_folder(self):
        from plone.dexterity.utils import createContentInContainer
        from zope.lifecycleevent import modified
        folder = createContentInContainer(
            self.portal, 'collective.behavior.stock.Folder', id='folder',
            checkConstraints=False, title='Földer', description='Description of Földer.')
        modified(folder)
        return folder

    def create_stockint(self, folder=None):
        from collective.behavior.stock.behavior import StockInt
        if folder is None:
            folder = self.create_folder()
        return StockInt(folder)

    def test_instance(self):
        from collective.behavior.stock.behavior import StockInt
        instance = self.create_stockint()
        self.assertIsInstance(instance, StockInt)

    def test_folder___catalog(self):
        from Products.CMFPlone.CatalogTool import CatalogTool
        from collective.behavior.stock.behavior import StockInt
        folder = self.create_folder()
        self.assertIsInstance(StockInt(folder)._catalog, CatalogTool)

    def test_folder___base_query(self):
        from Products.CMFPlone.CatalogTool import CatalogTool
        from collective.behavior.stock.behavior import StockInt
        folder = self.create_folder()
        self.assertEqual(StockInt(folder)._base_query, {
            'object_provides': 'collective.cart.stock.interfaces.IStock',
            'path': {'depth': 1, 'query': '/plone/folder'},
        })

    def test_instance__empty(self):
        from collective.behavior.stock.behavior import StockInt
        instance = self.create_stockint()
        self.assertEqual(instance, 0)

    def create_stock(self, folder, oid, stock):
        from plone.dexterity.utils import createContentInContainer
        from zope.lifecycleevent import modified
        obj = createContentInContainer(
            folder, 'collective.cart.stock.Stock', id=oid, stock=stock)
        modified(obj)
        obj.reindexObject()
        return obj

    def test_instance__one_stock(self):
        folder = self.create_folder()
        self.create_stock(folder, 'stock1', 100)
        instance = self.create_stockint(folder=folder)
        self.assertEqual(instance, 100)

    def test_instance__two_stocks(self):
        folder = self.create_folder()
        self.create_stock(folder, 'stock1', 100)
        self.create_stock(folder, 'stock2', 50)
        instance = self.create_stockint(folder=folder)
        self.assertEqual(instance, 150)

    def test__sub__ValueError(self):
        instance = self.create_stockint()
        with self.assertRaises(ValueError):
            instance - 3

    def test__sub__one_stock(self):
        folder = self.create_folder()
        stock1 = self.create_stock(folder, 'stock1', 100)
        instance = self.create_stockint(folder=folder)
        self.assertEqual(instance - 20, 80)
        self.assertEqual(stock1.stock, 80)

    def test__sub__multiple_stock(self):
        folder = self.create_folder()
        stock1 = self.create_stock(folder, 'stock1', 100)
        stock3 = self.create_stock(folder, 'stock3', 50)
        stock2 = self.create_stock(folder, 'stock2', 10)
        instance = self.create_stockint(folder=folder)
        self.assertEqual(instance - 20, 140)
        self.assertEqual(stock1.stock, 80)
        self.assertEqual(stock3.stock, 50)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance - 90, 50)
        self.assertEqual(stock1.stock, 0)
        self.assertEqual(stock3.stock, 40)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance - 30, 20)
        self.assertEqual(stock1.stock, 0)
        self.assertEqual(stock3.stock, 10)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance - 15, 5)
        self.assertEqual(stock1.stock, 0)
        self.assertEqual(stock3.stock, 0)
        self.assertEqual(stock2.stock, 5)
        with self.assertRaises(ValueError):
            instance - 20

    def test__add__ValueError(self):
        instance = self.create_stockint()
        with self.assertRaises(ValueError):
            instance + 3

    def test__add__one_stock(self):
        from zope.lifecycleevent import modified
        folder = self.create_folder()
        stock1 = self.create_stock(folder, 'stock1', 100)
        instance = self.create_stockint(folder=folder)
        with self.assertRaises(ValueError):
            instance + 3
        stock1.stock = 20
        modified(stock1)
        self.assertEqual(instance + 20, 40)
        self.assertEqual(stock1.stock, 40)
        with self.assertRaises(ValueError):
            instance + 100
        self.assertEqual(stock1.stock, 40)
        self.assertEqual(instance + 60, 100)
        self.assertEqual(stock1.stock, 100)

    def test__add__multiple_stock(self):
        from zope.lifecycleevent import modified
        folder = self.create_folder()
        stock1 = self.create_stock(folder, 'stock1', 100)
        stock3 = self.create_stock(folder, 'stock3', 50)
        stock2 = self.create_stock(folder, 'stock2', 10)
        instance = self.create_stockint(folder=folder)
        with self.assertRaises(ValueError):
            instance + 3
        stock1.stock = 20
        modified(stock1)
        stock3.stock = 10
        modified(stock3)
        stock2.stock = 5
        modified(stock2)
        self.assertEqual(instance + 2, 37)
        self.assertEqual(stock1.stock, 20)
        self.assertEqual(stock3.stock, 10)
        self.assertEqual(stock2.stock, 7)
        self.assertEqual(instance + 13, 50)
        self.assertEqual(stock1.stock, 20)
        self.assertEqual(stock3.stock, 20)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance + 40, 90)
        self.assertEqual(stock1.stock, 30)
        self.assertEqual(stock3.stock, 50)
        self.assertEqual(stock2.stock, 10)
        with self.assertRaises(ValueError):
            instance + 80
        self.assertEqual(stock1.stock, 30)
        self.assertEqual(stock3.stock, 50)
        self.assertEqual(stock2.stock, 10)
