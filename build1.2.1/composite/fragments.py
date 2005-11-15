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
from AccessControl import ClassSecurityInfo
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

# HTML Fragments should maintain reference information.
try:
    from Products.kupu.plone.ReftextField import ReftextField as TextField
except:
    pass
COMPOSITE = 'composite'

class Fragments(BaseContentMixin):

    meta_type = portal_type = 'CompositePack Fragments'
    archetype_name = 'Navigation Page HTML'
    global_allow = 0

    security = ClassSecurityInfo()

    idfield = MinimalSchema['id'].copy()
    idfield.widget.visible = {'edit':'hidden', 'view':'invisible'}

    schema = Schema((
        idfield,
        TextField(
            'content',
            accessor='getContent',
            allowable_content_types=('text/html','text/plain'),
            default_output_type='text/x-html-captioned',
            widget=RichWidget(
                label='Text or HTML',
                description='''Enter some text to be inserted into the containing page.''',
            )
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

    security.declareProtected(CMFCorePermissions.View, 'getContent')
    def getContent(self, mimetype=None, **kw):
        """Content accessor:
            If mimetype is text/plain, return as is.
            Otherwise return text/x-html-captioned (to replace embedded uids)
        """
        if kw.has_key('schema'):
            schema = kw['schema']
        else:
            schema = self.Schema()
            kw['schema'] = schema

        current_type = self.get_content_type('content')

        # Avoid converting plain text to html (use it as it is),
        # but HTML gets converted to remove embedded uids.
        if (not mimetype) and current_type == 'text/plain':
            return schema['content'].get(self, mimetype='text/plain', **kw)

        return schema['content'].get(self, **kw)

    def SearchableText(self):
        """Get text for indexing. Ignore the real mimetype, we want to do the
        conversion from HTML to plain text.
        """
        return ""

    def ContainerSearchableText(self):
        portal_transforms = getToolByName(self, 'portal_transforms')
        content = self.getRawContent()
        stream = portal_transforms.convertTo('text/plain', content, mimetype='text/html')
        return stream.getData()

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

registerType(Fragments, PROJECTNAME)