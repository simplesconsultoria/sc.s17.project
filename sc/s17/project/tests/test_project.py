# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI

from Products.CMFCore.utils import getToolByName

from sc.s17.project.project import IProject
from sc.s17.project.testing import INTEGRATION_TESTING


class TestClientIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        # overrides default behavior to make testing easier
        types = getToolByName(self.portal, 'portal_types')
        types['sc.s17.project.project'].global_allow = True

        self.folder.invokeFactory('sc.s17.project.project', 'obj')
        self.obj = self.folder['obj']

    def test_adding(self):
        self.folder.invokeFactory('sc.s17.project.project', 'project')
        project = self.folder['project']
        self.failUnless(IProject.providedBy(project))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='sc.s17.project.project')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='sc.s17.project.project')
        schema = fti.lookupSchema()
        self.assertEquals(IProject, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='sc.s17.project.project')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IProject.providedBy(new_object))

#    def test_allowed_content_types(self):
#        types = ['Image','File']
#        self.failUnlessEqual(self.obj.getLocallyAllowedTypes(), types)
#        self.failUnlessEqual(self.obj.getImmediatelyAddableTypes(), types)
#        self.assertRaises(ValueError,
#                          self.obj.invokeFactory, 'Document', 'foo')
#        try:
#            self.obj.invokeFactory('Image', 'foo')
#        except Unauthorized:
#            self.fail()

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)