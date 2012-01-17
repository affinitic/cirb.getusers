# -*- coding: UTF-8 -*-
import unittest2 as unittest
import cirb.getusers.browser.getusersview import Users

class TestUsers(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

    def test_users_list(self):
        #add users
        Users("membership")
