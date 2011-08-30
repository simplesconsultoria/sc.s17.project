import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite, onsetup

import sc.s17.project

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml',
                     sc.s17.project)

    fiveconfigure.debug_mode = False

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        
        @classmethod
        def tearDown(cls):
            pass
    
setup_product()
ptc.setupPloneSite()

def test_suite():
    return unittest.TestSuite([
        
        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='sc.s17.project',
        #    setUp=testing.setUp, tearDown=testing.tearDown),
        
        #doctestunit.DocTestSuite(
        #    module='sc.s17.project.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),
        
        
        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='sc.s17.project',
        #    test_class=TestCase),
        
        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='sc.s17.project',
        #    test_class=TestCase),
        
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
