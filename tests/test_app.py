import pytest
import unittest
from app import app
import os
from flask import session

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.secret_key = os.urandom(12)
        cls.app = app.test_client()

    @pytest.mark.inject
    def test_successful_login(self):
        res = self.app.post("/home", data=dict(username="admin", inputPassword="jd"))
        self.assertTrue("Your Feedback" in str(res.data), msg="Login did not happen even with correct credentials")

    @pytest.mark.inject
    def test_invalid_credential_login(self):
        res = self.app.post("/home", data=dict(username="admin", inputPassword="test"))
        self.assertTrue("No user found" in str(res.data), msg="Login happened even with incorrect credentials")

    @pytest.mark.inject
    def test_injection(self):
        res = self.app.post("/home", data=dict(username="Electrician", inputPassword="a' or 1=1; -- com"))
        self.assertFalse("Your Feedback" in str(res.data), msg="SQL injection exists in the application")