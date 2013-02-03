# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from collective.behavior.stock.tests.base import IntegrationTestCase


class TestSetup(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_collective_behavior_stock_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('collective.behavior.stock'))

    def test_is_collective_cart_stock_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('collective.cart.stock'))

    def test_catalog__initial_stock(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        self.assertIn('initial_stock', catalog.schema())

    def test_catalog__stock(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        self.assertIn('stock', catalog.schema())

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(setup.getVersionForProfile(
            'profile-collective.behavior.stock:default'), u'0')

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.behavior.stock'])
        self.failIf(installer.isProductInstalled('collective.behavior.stock'))
