# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import IConstrainTypes

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

    def test_allowed_content_types(self):
        types = ['File', 'Image']

        # test allowed content types
        allowed_types = [t.getId() for t in self.obj.allowedContentTypes()]
        for t in types:
            self.failUnless(t in allowed_types)

        # test addable content types on menu
        constrain = IConstrainTypes(self.obj, None)
        if constrain:
            immediately_addable_types = constrain.getLocallyAllowedTypes()
            for t in types:
                self.failUnless(t in immediately_addable_types)

        # trying to add any other content type raises an error
        self.assertRaises(ValueError,
                          self.obj.invokeFactory, 'Document', 'foo')

        try:
            self.obj.invokeFactory('File', 'foo')
            self.obj.invokeFactory('Image', 'bar')
        except Unauthorized:
            self.fail()


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
