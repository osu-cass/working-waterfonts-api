from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Group


class LoginViewTestCase(TestCase):

    """
    Test the login view:
        1. the url resolves properly
        2. test that a bad login returns an invalid username/password message
        3. test that a good login without a 'next' tag forwards to the
            expected destination
        4. test that a good login with a 'next' tag forwards to the 'next'
            destination
    """

    def setUp(self):
        self.user_credentials = {
            'username': 'dataentry',
            'password': 'password'}
        self.user = User.objects.create_user(
            self.user_credentials['username'],
            'data@example.com',
            self.user_credentials['password'])
        self.user.save()

    def test_url_endpoint(self):
        url = reverse('login')
        self.assertEqual(url, '/login')

    def test_bad_login(self):
        """
        POST a login command to the server with a bad user/bad password and see
        if we get logged in
        """
        bad_password = {
            'username': self.user_credentials['username'],
            'password': 'bad_password'
        }

        response = self.client.post(
            reverse('login'), bad_password, follow=True)

        self.assertContains(
            response, "Invalid username or password")

        bad_username = {
            'username': 'bad_dataentry',
            'password': self.user_credentials['password']
        }

        response = self.client.post(
            reverse('login'), bad_username, follow=True)

        self.assertContains(
            response, "Invalid username or password")

    def test_good_password(self):
        """
        POST a login command to the server with a good user and see if
        we get logged in
        """
        response = self.client.post(
            reverse('login'), self.user_credentials)
        self.assertRedirects(response, '/entry')

    def test_redirect(self):
        """
        POST a login command to the server with a good user and a 'next'
        parameter, and see if we get logged in
        """
        post_data = self.user_credentials.copy()
        post_data['next'] = '/entry/pois/'

        response = self.client.post(
            reverse('login'), post_data)
        self.assertRedirects(response, '/entry/pois/')

    def test_root_redirect(self):
        """
        GET the root of the site ('/'), and verify that it correctly
        redirects to the login page ('/login').
        """
        response = self.client.get('/')
        self.assertRedirects(response, '/login')

    def test_logged_in_redirect(self):
        """
        Log into the site ('/login'), and then GET '/login' again to
        verify that it redirects.
        """
        self.client.post(reverse('login'), self.user_credentials)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, '/entry')
