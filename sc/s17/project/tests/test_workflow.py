# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

from sc.s17.client.testing import INTEGRATION_TESTING

ctype = 'sc.s17.project'
workflow_id = 'project_workflow'


class WorkflowTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow_tool = getattr(self.portal, 'portal_workflow')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        # overrides default behavior to make testing easier
        types = getToolByName(self.portal, 'portal_types')
        types[ctype].global_allow = True

        self.folder.invokeFactory(ctype, 'obj')
        self.obj = self.folder['obj']

    def test_workflow_installed(self):
        ids = self.workflow_tool.getWorkflowIds()
        self.failUnless(workflow_id in ids)

    def test_default_workflow(self):
        chain = self.workflow_tool.getChainForPortalType(self.obj.portal_type)
        self.failUnless(len(chain) == 1)
        self.failUnless(chain[0] == workflow_id)

    def test_workflow_initial_state(self):
        status = self.workflow_tool.getStatusOf(workflow_id, self.obj)
        self.failUnless(status['review_state'] == 'open')

    def test_workflow_transitions(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'close')
        status = self.workflow_tool.getStatusOf(workflow_id, self.obj)
        self.failUnless(status['review_state'] == 'closed')
        self.workflow_tool.doActionFor(self.obj, 'reopen')
        status = self.workflow_tool.getStatusOf(workflow_id, self.obj)
        self.failUnless(status['review_state'] == 'open')

    def test_workflow_permissions(self):
        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'close')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'close')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'reopen')
