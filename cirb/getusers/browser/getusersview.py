from zope.interface import implements, Interface
from zope.app.component.hooks import getSite

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from cirb.getusers import getusersMessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import csv

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
        site = getSite()
        return [r for r in site.portal_membership.getPortalRoles() if r != 'Owner'] 

    def update_users(self):
        for member in self.membership.listMembers():
            # add email
            user = {}
            user['name'] = member.getProperty('fullname', member.getUserName())
            user['email'] = member.getProperty('email', None)
            if self.roles:
                user['roles'] = member.getRoles()
            self.append(user)
    
    def get_users(self):
        return self

    def get_csv_users(self):
        from StringIO import StringIO
        buf = StringIO()
        writer = csv.writer(buf, dialect='excel', delimiter=";")
        writer.writerow(self.get_csv_first_line())
        for user in self:
            col = []
            col.append(user.get('name'))
            col.append(user.get('email'))
            if self.roles:
                for role in self.plone_roles:
                    if role in user.get('roles', []):
                        col.append("X")
                    else:
                        col.append("")
            writer.writerow(col)
        return buf.getvalue()
    
    def get_csv_first_line(self):
        #TODO get translation
        results = ['Name', 'Email']
        if self.roles:
            for r in self.plone_roles:
                results.append(r)
        return results
            

class GetUsers(BrowserView):
    def  __init__(self, context, request):
        self.context = context
        self.request = request
        self.membership = getToolByName(context, "portal_membership")

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
        RESPONSE.setHeader("Content-disposition","attachment;filename=PloneUsers.csv")
