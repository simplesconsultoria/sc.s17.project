# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from sc.s17.client.config import PROJECTNAME
from sc.s17.client.testing import INTEGRATION_TESTING

# TODO: review real dependencies
PRODUCT_DEPENDENCIES = []


class TestInstall(unittest.TestCase):
    """ensure product is properly installed"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = getattr(self.portal, 'portal_quickinstaller')

    def test_installed(self):
        self.failUnless(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_dependencies_installed(self):
        for p in PRODUCT_DEPENDENCIES:
            self.failUnless(self.qi.isProductInstalled(p),
                            '%s not installed' % p)


class TestUninstall(unittest.TestCase):
    """ensure product is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
