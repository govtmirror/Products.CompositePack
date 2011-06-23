##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""
$Id$
"""
# Load fixture
from Products.PloneTestCase import PloneTestCase


## LinguaPlone addon?
try:
    from Products.LinguaPlone.public import registerType
except ImportError:
    HAS_LINGUA_PLONE = False
else:
    HAS_LINGUA_PLONE = True
    del registerType


DEPENDENCIES = (
    'Archetypes',
    'MimetypesRegistry',
    'PortalTransforms',
    'ATContentTypes',
    'kupu',
    'GenericSetup',
    'CompositePack',
    'CompositePage',
)

[PloneTestCase.installProduct(dep, quiet=1) for dep in DEPENDENCIES]

# Install our product
if HAS_LINGUA_PLONE:
    PloneTestCase.installProduct('PloneLanguageTool')


PloneTestCase.setupPloneSite()


class CompositePackTestCase(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        from Products.CMFCore.utils import getToolByName
        from Products.CompositePack.config import get_ATCT_TYPES
        from Products.CompositePack.config import HAS_GS
        super(PloneTestCase.PloneTestCase, self).afterSetUp()
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')
        if HAS_GS:
            self.gs = getToolByName(self.portal, 'portal_setup')

        if HAS_LINGUA_PLONE:
            self.qi.installProduct('PloneLanguageTool')
        self.qi.installProduct('ATContentTypes')
        self.qi.installProduct('kupu')
        self.installCompositePack()

        self.composite_tool = getToolByName(self.portal, 'composite_tool')
        self.FILE_TYPE = get_ATCT_TYPES(self.portal)['File']
        self.EVENT_TYPE = get_ATCT_TYPES(self.portal)['Event']
        self.FAVORITE_TYPE = get_ATCT_TYPES(self.portal)['Favorite']

    def installCompositePack(self):
        self.qi.installProduct('CompositePack')

    def beforeTearDown(self):
        self.composite_tool.clearLayoutRegistry()
        self.composite_tool.clearViewletRegistry()
        super(PloneTestCase.PloneTestCase, self).beforeTearDown()