# -*- coding: UTF-8 -*-
import unittest2 as unittest
from cirb.getusers.browser.getusersview import Users

class TestUsers(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

    def test_excel_first_line(self):
        #membership = getToolByName(self, "portal_membership")
        u = Users()
        self.assertEqual(u.get_excel_first_line, '', 'Excel first line not correct')
        #add users
        
