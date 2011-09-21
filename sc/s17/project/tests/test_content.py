# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI

from Products.CMFCore.utils import getToolByName

from sc.s17.project.content import IProject
from sc.s17.project.testing import INTEGRATION_TESTING

ctype = 'sc.s17.project'


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        # overrides default behavior to make testing easier
        types = getToolByName(self.portal, 'portal_types')
        types[ctype].global_allow = True

        self.folder.invokeFactory(ctype, 'obj')
        self.obj = self.folder['obj']

    def test_adding(self):
        self.failUnless(IProject.providedBy(self.obj))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name=ctype)
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name=ctype)
        schema = fti.lookupSchema()
        self.assertEquals(IProject, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name=ctype)
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IProject.providedBy(new_object))

    def test_view(self):
        self.obj.restrictedTraverse('@@view')


class GlobalAllowTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_disallowed(self):
        # test normal behavior of global_allow=False as declared on XML
        self.assertRaises(ValueError, self.folder.invokeFactory, ctype, 'obj')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
