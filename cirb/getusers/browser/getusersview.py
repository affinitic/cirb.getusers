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
    roles = Choice(title=u'Roles', vocabulary='Available Roles', required=True, default="True")
    output = Choice(title=u'Output', vocabulary='Available Outputs', required=True, default="Excel")
    
def availableRoles(context):
    subjects = (_(u'True'), _(u'False'), )
    return SimpleVocabulary.fromValues(subjects)

def availableOutputs(context):
    #subjects = (_(u'Excel'), _(u'Pdf'), )
    subjects = (_(u'Excel'),)
    return SimpleVocabulary.fromValues(subjects)


class Users(list):
    """
    Get Users from plone site
    """
    def __init__(self, membership, roles=False):
        self.membership = membership
        if roles == "False" or roles == "Non" or roles == "Nee":
            self.roles = False
        else:
            self.roles = True
        self.plone_roles = [(0,'Authenticated'), (1,'Site Administrator'), (2,'Member'), (3,'Manager'), (4,'Editor'), (5,'Reader'), (6,'Contributor'), (7,'Reviewer')]
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

    def get_excel_users(self):
        users = "%s\n" % self.get_excel_first_line()
        for user in self:
            users += "%s;" % user.get('name')
            if self.roles:
                xls_roles = ["" for x in range(len(self.plone_roles))]
                for role in user.get('roles'):
                    for k, v in self.plone_roles:
                        if role == v:
                            xls_roles[k] = "X"
                    
                users += ";".join(xls_roles)
            users += "\n"
        return users
    
    def get_excel_first_line(self):
        #TODO get translation
        results = ['Name']
        if self.roles:
            for k, v in sorted(self.plone_roles):
                results.append(v)
        return ";".join(results)
            


class GetUsersForm(PageForm):
    label = _('Get user list')
    form_fields = form.Fields(IGetUsersForm)
    template = ViewPageTemplateFile('getusersview.pt')

    
    @form.action("send")
    def action_send(self, action, data):
        roles = data.get('roles', False)
        membership = getToolByName(self, "portal_membership")
        RESPONSE = self.request.response
        users = Users(membership, roles)
        if data.get('output').lower() == "excel":
            RESPONSE.setHeader("Content-type","application/ms-excel")
            RESPONSE.setHeader("Content-disposition","attachment;filename=Users.xls")

        return users.get_excel_users()
