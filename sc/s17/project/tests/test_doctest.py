# -*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from sc.s17.project.testing import FUNCTIONAL_TESTING

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/functional.txt',
                                     package='sc.s17.project',
                                     optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        ])
    return suite
