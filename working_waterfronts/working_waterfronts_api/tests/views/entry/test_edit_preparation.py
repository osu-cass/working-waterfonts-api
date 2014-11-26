from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Preparation
from django.contrib.auth.models import User, Group


class EditPreparationTestCase(TestCase):

    """
    Test that the Edit Preparation page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the preparation
            object with the specified ID
    """
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        response = self.client.login(
            username='temporary', password='temporary')
        self.assertEqual(response, True)

    def test_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse('edit-preparation', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/preparations/1')

    def test_url_endpoint(self):
        url = reverse('edit-preparation', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/preparations/1')

    def test_successful_preparation_update(self):
        """
        POST a proper "update preparation" command to the server, and see if
        the update appears in the database
        """
        # Data that we'll post to the server to get the new preparation created
        new_preparation = {
            'name': u'Fried', 'description': u'', 'additional_info': u''}

        self.client.post(
            reverse('edit-preparation', kwargs={'id': '1'}),
            new_preparation)

        preparation = Preparation.objects.get(id=1)
        for field in new_preparation:
            self.assertEqual(
                getattr(preparation, field), new_preparation[field])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(
            reverse('edit-preparation', kwargs={'id': '1'}))

        fields = {
            'name': u'Live',
            'description': u'The food goes straight from sea \
to you with live food, sitting in saltwater tanks!',
            'additional_info': u'Live octopus requires a locking container'
        }

        form = response.context['preparation_form']

        for field in fields:
            self.assertEqual(fields[field], form[field].value())

    def test_delete_preparation(self):
        """
        Tests that DELETing entry/preparations/<id> deletes the item
        """
        response = self.client.delete(
            reverse('edit-preparation', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Preparation.DoesNotExist):
            Preparation.objects.get(id=2)

        response = self.client.delete(
            reverse('edit-preparation', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 404)
