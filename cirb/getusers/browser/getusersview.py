from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from cirb.getusers import getusersMessageFactory as _

from zope.schema import TextLine, Text, Choice
from zope.formlib import form
from zope.schema.vocabulary import SimpleVocabulary
from five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IGetUsersForm(Interface):
    """
    Get Users view interface
    """
    roles = Choice(title=u'Roles', vocabulary='Available Roles', required=False)
    output = Choice(title=u'Output', vocabulary='Available Outputs', required=True)
    
def availableRoles(context):
    subjects = (True, False, )
    return SimpleVocabulary.fromValues(subjects)

def availableOutputs(context):
    subjects = ('Excel', 'Pdf', )
    return SimpleVocabulary.fromValues(subjects)


class Users(list):
    """
    Get Users from plone site
    """
    def __init__(self, membership, roles=False):
        self.membership = membership
        self.roles = roles
        self.update_users()
    
    def update_users(self):
        for member in self.membership.listMembers():
            # add email
            item = {}
            item['name'] = member.getUserName()
            if self.roles:
                item['roles'] = member.getRoles()
            self.append(item)       

    def get_users(self):
        return self
    

class GetUsersForm(PageForm):
    label = _('Get user list')
    form_fields = form.Fields(IGetUsersForm)
    template = ViewPageTemplateFile('getusersview.pt')
    
    @form.action("send")
    def action_send(self, action, data):
        roles = data['roles']
        return Users(getToolByName(self, 'portal_membership'), roles).get_users()