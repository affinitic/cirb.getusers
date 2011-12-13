from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from cirb.getusers import getusersMessageFactory as _


class IGetUsersView(Interface):
    """
    Get Users view interface
    """

    def test():
        """ test method"""


class GetUsersView(BrowserView):
    """
    Get Users browser view
    """
    implements(IGetUsersView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')
        return {'dummy': dummy}

    def get_users(self):
        users=[]
        membership = getToolByName(self, 'portal_membership')
        for member in membership.listMembers():
            # add email
            users.append({'name':member.getUserName(),'roles':member.getRoles()})
        return users
