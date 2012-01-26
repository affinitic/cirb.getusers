# -*- coding: UTF-8 -*-
import unittest2 as unittest
from cirb.getusers.browser.getusersview import Users
from cirb.getusers.testing import GETUSERS_INTEGRATION

from plone.app.testing.interfaces import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES
from Products.CMFCore.utils import getToolByName

import csv
from StringIO import StringIO
class TestUsers(unittest.TestCase):
    layer = GETUSERS_INTEGRATION

    def test_csv_return(self):
        portal = self.layer["portal"]
        pas = portal['acl_users']
        pas.source_users.addUser("dummy_userid", "dummy_username", TEST_USER_PASSWORD, )
        membership = getToolByName(portal, "portal_membership") 
        member = membership.getMemberById('dummy_userid')
        member.setMemberProperties({'fullname':'dummy', "email":"dummy@user.id"})
        u = Users(membership, False)
        self.assertEqual(u.get_csv_users(), "Name;Email\r\ndummy;dummy@user.id\r\n;\r\n", 'Number of csv lines is incorrect')
       

    def test_cross(self):
        portal = self.layer["portal"]
        pas = portal['acl_users']
        pas.source_users.addUser("dummy_userid", "dummy_username", TEST_USER_PASSWORD, )
        for role in TEST_USER_ROLES:
            pas.portal_role_manager.doAssignRoleToPrincipal("dummy_userid", role)
        membership = getToolByName(portal, "portal_membership") 
        member = membership.getMemberById('dummy_userid')
        member.setMemberProperties({'fullname':'dummy', "email":"dummy@user.id"})
        u = Users(membership, True)
        dr = csv.DictReader(StringIO(u.get_csv_users()), delimiter=";")
        users_list = list(dr)
        self.assertEqual(len(users_list),2)
        self.assertEqual(users_list[0].get('Member'), "X")
        self.assertNotEqual(users_list[1].get('Manager'), "X")

