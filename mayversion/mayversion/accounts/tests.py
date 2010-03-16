"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from mayversion.accounts.models import UserProfile,UserMoreProfile

class SimpleTest(TestCase):

    def test_userProfileHasMoreProfile(self):
        u = UserProfile.objects.get(pk = 1)
        self.assertEqual(u.user.username,'peter')
        self.assertTrue(u.get_more_profile())

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Test UserProfile get More Profile
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

