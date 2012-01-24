from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from cirb.getusers import getusersMessageFactory as _

from zope.schema import TextLine, Text, Choice
from zope.formlib import form
from zope.schema.vocabulary import SimpleVocabulary
from five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Users(list):
    """
    Get Users from plone site
    """
    def __init__(self, membership, roles):
        self.membership = membership
        self.roles = roles
        self.plone_roles = self.get_plone_roles()
        self.update_users()
   
    def get_plone_roles(self):
        return ['Authenticated', 'Site Administrator', 'Member', 'Manager', 'Editor','Reader', 'Contributor', 'Reviewer']

    def update_users(self):
        for member in self.membership.listMembers():
            # add email
            item = {}
            item['name'] = member.getUserName()
            item['email'] = member.getProperty('email', None)
            if self.roles:
                item['roles'] = member.getRoles()
            self.append(item)
    
    def get_users(self):
        return self

    def get_csv_users(self):
        users = "%s\n" % self.get_csv_first_line()
        for user in self:
            users += "%s;" % user.get('name')
            users += "%s;" % user.get('email')
            if self.roles:
                xls_roles = ["" for x in range(len(self.plone_roles))]
                for role in user.get('roles'):
                    for r in self.plone_roles:
                        if role == r:
                            xls_roles[self.plone_roles.index(r)] = "X"
                    
                users += ";".join(xls_roles)
            users += "\n"
        return users
    
    def get_csv_first_line(self):
        #TODO get translation
        results = ['Name', 'Email']
        if self.roles:
            for r in self.plone_roles:
                results.append(r)
        return ";".join(results)
            


class GetUsers(BrowserView):
    def  __init__(self, context, request):
        self.context = context
        self.request = request
        self.membership = getToolByName(self, "portal_membership")
    
    def get_view(self):
        return {"view":"view"}

    #TODO add an args (role) in view
    def get_users(self):
        roles = False
        if self.request.form.get('roles') == "true":
            roles = True
        self.set_excel_response(self.request.response)
        users = Users(self.membership, roles)
        return users.get_csv_users()

    def set_excel_response(self, RESPONSE):
        RESPONSE.setHeader("Content-type","application/ms-excel")
        RESPONSE.setHeader("Content-disposition","attachment;filename=UsersFromPloneSite.csv")

