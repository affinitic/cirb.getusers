# -*- coding: UTF-8 -*-
import unittest2 as unittest
from cirb.getusers.browser.getusersview import Users
from cirb.getusers.testing import GETUSERS_INTEGRATION

class TestUsers(unittest.TestCase):
    layer = GETUSERS_INTEGRATION
    def test_dummy(self):
        self.assertTrue(True)

    def test_excel_first_line(self):
        portal = self.layer["portal"]
        #import pdb; pdb.set_trace()
        #membership = self.layer["portal_membership"]
        #print membership
        u = Users()
        self.assertEqual(u.get_excel_first_line, '', 'Excel first line not correct')
        #add users
        
