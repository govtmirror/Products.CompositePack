##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Navigation Page :

$Id: navigationpage.py,v 1.3 2004/08/25 17:02:02 godchap Exp $
"""

from Products.Archetypes.public import BaseSchema

from Products.CompositePack.config import PROJECTNAME
from Products.CompositePack.composite import packcomposite
from Products.CompositePack.public import BaseContent, registerType

class NavigationPage(BaseContent):
    """A basic, Archetypes-based Composite Page
    """
    meta_type = portal_type = 'Navigation Page'
    archetype_name = 'Navigation Page'
    schema = BaseSchema
    actions = packcomposite.actions
    
    factory_type_information={
            'content_icon':'composite.gif',
            }

registerType(NavigationPage, PROJECTNAME)
