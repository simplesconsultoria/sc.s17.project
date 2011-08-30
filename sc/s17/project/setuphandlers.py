# -*- coding: utf-8 -*-
from zope import component
import logging
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup import interfaces as gsinterfaces
from Products.GenericSetup.upgrade import listUpgradeSteps

from Products.ZCatalog.ProgressHandler import ZLogHandler

try:
    from Products.CacheSetup import interfaces
    from Products.CacheSetup.enabler import enableCacheFu
    CACHEFU = True
except ImportError:
    CACHEFU = False

_PROJECT = 'sc.s17.project'
_PROFILE_ID = 'sc.s17.project:default'


def doUpgrades(context):
    """ If exists, run migrations
    """
    if context.readDataFile('sc.s17.project.txt') is None:
        return
    logger = logging.getLogger(_PROJECT)
    site = context.getSite()
    setup_tool = getToolByName(site,'portal_setup')
    cache = CACHEFU and getToolByName(context,'portal_cache_settings',None)
    version = setup_tool.getLastVersionForProfile(_PROFILE_ID)
    upgradeSteps = listUpgradeSteps(setup_tool,_PROFILE_ID, version)
    sorted(upgradeSteps,key=lambda step:step['sortkey'])

    if cache:
        # Disable cachefu to avoid a tsunami of purge requests
        cache.setEnabled(False)

    for step in upgradeSteps:
        oStep = step.get('step')
        if oStep is not None:
            oStep.doStep(setup_tool)
            msg = "Ran upgrade step %s for profile %s" % (oStep.title,
                                                          _PROFILE_ID)
            setup_tool.setLastVersionForProfile(_PROFILE_ID, oStep.dest)
            logger.info(msg)

    if cache:
        # Its ok to enable it again
        cache.setEnabled(True)

