# -*- coding: utf-8 -*-
from collective.behavior.stock.tests.base import IntegrationTestCase

import mock


class TestStock(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']

    def test_subclass(self):
        from collective.behavior.stock.behavior import Stock
        self.assertTrue(issubclass(Stock, object))

    def create_folder(self):
        from plone.dexterity.utils import createContentInContainer
        from zope.lifecycleevent import modified
        folder = createContentInContainer(
            self.portal, 'collective.behavior.stock.Folder', id='folder',
            checkConstraints=False, title='Földer', description='Description of Földer.')
        modified(folder)
        return folder

    def create_instance(self, folder=None):
        from collective.behavior.stock.interfaces import IStock
        if folder is None:
            folder = self.create_folder()
        return IStock(folder)

    def test_instance(self):
        from collective.behavior.stock.behavior import Stock
        instance = self.create_instance()
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
        from plone.dexterity.content import Container
        instance = self.create_instance()
        self.assertIsInstance(instance.context, Container)

    def test_instance__reducible_quantity_empty(self):
        """First time access to reducible_quantity"""
        instance = self.create_instance()
        self.assertEqual(instance.reducible_quantity, 0)

    def test_instance__reducible_quantity__ValueError(self):
        """Raise ValueError when setting other than integer."""
        instance = self.create_instance()
        with self.assertRaises(ValueError):
            instance.reducible_quantity = 'AAA'

    def test_instance__reducible_quantity__set(self):
        instance = self.create_instance()
        reducible_quantity = 5
        instance.reducible_quantity = reducible_quantity
        self.assertEqual(instance.context.reducible_quantity, reducible_quantity)

    @mock.patch('collective.behavior.stock.behavior.getToolByName')
    def test_stocks(self, getToolByName):
        instance = self.create_instance()
        instance.stocks()
        getToolByName().assert_called_with({
            'path': {
                'query': '/plone/folder',
                'depth': 1,
            },
            'object_provides': 'collective.cart.stock.interfaces.IStock',
            'sort_on': 'getObjPositionInParent',
            'sort_order': 'ascending',
        })

    @mock.patch('collective.behavior.stock.behavior.getToolByName')
    def test_stocks_descending(self, getToolByName):
        instance = self.create_instance()
        instance.stocks(sort_order='descending')
        getToolByName().assert_called_with({
            'path': {
                'query': '/plone/folder',
                'depth': 1,
            },
            'object_provides': 'collective.cart.stock.interfaces.IStock',
            'sort_on': 'getObjPositionInParent',
            'sort_order': 'descending',
        })

    def test_stock__empty(self):
        instance = self.create_instance()
        self.assertEqual(instance.stock(), 0)

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
        instance = self.create_instance(folder=folder)
        self.assertEqual(instance.initial_stock(), 100)
        self.assertEqual(instance.stock(), 100)

    def test_instance__two_stocks(self):
        folder = self.create_folder()
        self.create_stock(folder, 'stock1', 100)
        self.create_stock(folder, 'stock2', 50)
        instance = self.create_instance(folder=folder)
        self.assertEqual(instance.initial_stock(), 150)
        self.assertEqual(instance.stock(), 150)

    def test_sub_stock_more_than_available(self):
        instance = self.create_instance()
        self.assertEqual(instance.sub_stock(3), 0)
        self.assertEqual(instance.initial_stock(), 0)
        self.assertEqual(instance.stock(), 0)

    def test_sub_stock_one_stock(self):
        folder = self.create_folder()
        stock1 = self.create_stock(folder, 'stock1', 100)
        instance = self.create_instance(folder=folder)
        self.assertEqual(instance.initial_stock(), 100)
        self.assertEqual(instance.stock(), 100)

        self.assertEqual(instance.sub_stock(20), 20)
        self.assertEqual(stock1.stock, 80)
        self.assertEqual(instance.initial_stock(), 100)
        self.assertEqual(instance.stock(), 80)

    def test_sub_stock_multiple_stock(self):
        folder = self.create_folder()
        stock1 = self.create_stock(folder, 'stock1', 100)
        stock3 = self.create_stock(folder, 'stock3', 50)
        stock2 = self.create_stock(folder, 'stock2', 10)
        instance = self.create_instance(folder=folder)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 160)

        self.assertEqual(instance.sub_stock(20), 20)
        self.assertEqual(stock1.stock, 80)
        self.assertEqual(stock3.stock, 50)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 140)

        self.assertEqual(instance.sub_stock(90), 90)
        self.assertEqual(stock1.stock, 0)
        self.assertEqual(stock3.stock, 40)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 50)

        self.assertEqual(instance.sub_stock(30), 30)
        self.assertEqual(stock1.stock, 0)
        self.assertEqual(stock3.stock, 10)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 20)

        self.assertEqual(instance.sub_stock(15), 15)
        self.assertEqual(stock1.stock, 0)
        self.assertEqual(stock3.stock, 0)
        self.assertEqual(stock2.stock, 5)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 5)

        self.assertEqual(instance.sub_stock(20), 5)
        self.assertEqual(stock1.stock, 0)
        self.assertEqual(stock3.stock, 0)
        self.assertEqual(stock2.stock, 0)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 0)

    def test_add_stock_more_than_available(self):
        instance = self.create_instance()
        self.assertEqual(instance.add_stock(3), 0)
        self.assertEqual(instance.initial_stock(), 0)
        self.assertEqual(instance.stock(), 0)

    def test_add_stock_one_stock(self):
        from zope.lifecycleevent import modified
        folder = self.create_folder()
        stock1 = self.create_stock(folder, 'stock1', 100)
        instance = self.create_instance(folder=folder)
        self.assertEqual(instance.add_stock(3), 0)
        self.assertEqual(instance.initial_stock(), 100)
        self.assertEqual(instance.stock(), 100)
        stock1.stock = 20
        modified(stock1)
        self.assertEqual(instance.add_stock(20), 20)
        self.assertEqual(instance.initial_stock(), 100)
        self.assertEqual(instance.stock(), 40)
        self.assertEqual(stock1.stock, 40)
        self.assertEqual(instance.add_stock(100), 60)
        self.assertEqual(instance.initial_stock(), 100)
        self.assertEqual(stock1.stock, 100)

    def test_add_stock_multiple_stock(self):
        from zope.lifecycleevent import modified
        folder = self.create_folder()
        stock1 = self.create_stock(folder, 'stock1', 100)
        stock3 = self.create_stock(folder, 'stock3', 50)
        stock2 = self.create_stock(folder, 'stock2', 10)
        instance = self.create_instance(folder=folder)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 160)
        self.assertEqual(instance.add_stock(3), 0)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 160)

        stock1.stock = 20
        modified(stock1)
        stock3.stock = 10
        modified(stock3)
        stock2.stock = 5
        modified(stock2)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 35)

        self.assertEqual(instance.add_stock(2), 2)
        self.assertEqual(stock1.stock, 20)
        self.assertEqual(stock3.stock, 10)
        self.assertEqual(stock2.stock, 7)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 37)

        self.assertEqual(instance.add_stock(13), 13)
        self.assertEqual(stock1.stock, 20)
        self.assertEqual(stock3.stock, 20)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 50)

        self.assertEqual(instance.add_stock(40), 40)
        self.assertEqual(stock1.stock, 30)
        self.assertEqual(stock3.stock, 50)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 90)

        self.assertEqual(instance.add_stock(80), 70)
        self.assertEqual(stock1.stock, 100)
        self.assertEqual(stock3.stock, 50)
        self.assertEqual(stock2.stock, 10)
        self.assertEqual(instance.initial_stock(), 160)
        self.assertEqual(instance.stock(), 160)
