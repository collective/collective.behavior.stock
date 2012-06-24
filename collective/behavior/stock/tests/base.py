"""Base module for unittesting"""
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import unittest


class BehaviorStockLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import collective.behavior.stock
        self.loadZCML(package=collective.behavior.stock)
        z2.installProduct(app, 'collective.behavior.stock')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.behavior.stock:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'collective.behavior.stock')


FIXTURE = BehaviorStockLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="BehaviorStockLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="BehaviorStockLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
