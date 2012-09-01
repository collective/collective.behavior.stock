"""Base module for unittesting"""
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import unittest


class BehaviorStockLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import collective.behavior.stock
        self.loadZCML(package=collective.behavior.stock)
        import collective.behavior.stock.tests.dexterity
        self.loadZCML(package=collective.behavior.stock.tests.dexterity)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.behavior.stock:default')
        self.applyProfile(portal, 'collective.behavior.stock.tests.dexterity:default')

    def tearDownZope(self, app):
        """Tear down Zope."""


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
