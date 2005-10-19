##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Composite Titles :
   used to mix titles and composite elements in composite pages

$Id$
"""
from Products.Archetypes.public import *
from Products.CompositePack.config import PROJECTNAME
from Products.CMFCore.utils import getToolByName

COMPOSITE = 'composite'

class Titles(BaseContentMixin):

    meta_type = portal_type = 'CompositePack Titles'
    archetype_name = 'Navigation Titles'
    global_allow = 0

    _at_rename_after_creation = True
    
    idfield = MinimalSchema['id'].copy()
    idfield.widget.visible = {'edit':'hidden', 'view':'invisible'}

    schema = Schema((
        idfield,
        MinimalSchema['title'],
        StringField(
        'description',
        widget=StringWidget(label='Description',
                            description=('Description used as a subtitle.'))
        ),
        ReferenceField(
        'composite',
        relationship=COMPOSITE,
        widget=ReferenceWidget(label='Composite',
                               visible={'edit':'invisible',
                                        'view':'invisible'},
                            description=('Composite page containing this title.'))
        ),
        ))

    actions=  (
           {'action':      '''string:$object_url/../../../design_view''',
            'category':    '''object''',
            'id':          'view',
            'name':        'view',
            'permissions': ('''View''',)},

           )

    def SearchableText(self):
        '''Titles shouldn't be indexed in their own right'''
        return None

    def ContainerSearchableText(self):
        """Get text for indexing. Ignore the real mimetype, we want to do the
        conversion from HTML to plain text.
        """
        return self.Title() + '\n' + self.getDescription()

    def indexObject(self):
        '''Titles are never catalogued'''
        self._v__indexable = True

    def isTemporaryObject(self):
        return self.portal_factory.isTemporary(self)

    def reindexObject(self, idxs=[]):
        '''Titles are never catalogued, but container is'''
	if not self.isTemporaryObject():
            parent = self.aq_parent.aq_parent.aq_parent
            parent.reindexObject()

    def unindexObject(self):
        '''the parent will need reindexing'''
        # Set a volatile attribute to prevent this object being
        # indexed.
        self._v__indexable = False
        self.reindexObject()

    def dereferenceComposite(self):
        """Returns the object referenced by this composite element.
        """
        refs = self.getRefs(COMPOSITE)
        return refs and refs[0] or None

registerType(Titles, PROJECTNAME)