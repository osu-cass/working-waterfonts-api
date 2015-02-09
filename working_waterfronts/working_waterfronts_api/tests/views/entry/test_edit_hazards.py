from django.test import TestCase
from django.core.urlresolvers import reverse
from working_waterfronts.working_waterfronts_api.models import Hazard
from django.contrib.auth.models import User, Group


class EditHazardTestCase(TestCase):

    """
    Test that the Edit Hazard page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the hazard
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
            reverse('edit-hazard', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/hazards/1')

    def test_url_endpoint(self):
        url = reverse('edit-hazard', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/hazards/1')

    def test_successful_hazard_update(self):
        """
        POST a proper "update hazard" command to the server, and see if
        the update appears in the database
        """
        # Data that we'll post to the server to get the new hazard created
        new_hazard = {
            "name": "Alien Abduction Reloaded",
            "description": "This site is liable to result \
                in you being abducted by aliens, and now it's worse."
        }

        self.client.post(
            reverse('edit-hazard', kwargs={'id': '1'}),
            new_hazard)

        hazard = Hazard.objects.get(id=1)
        for field in new_hazard:
            self.assertEqual(
                getattr(hazard, field), new_hazard[field])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(
            reverse('edit-hazard', kwargs={'id': '1'}))

        fields = {
            "name": "Falling Rocks",
            "description": "If these fall on you, you're dead.",
        }

        form = response.context['hazard_form']

        for field in fields:
            self.assertEqual(fields[field], form[field].value())

    def test_delete_hazard(self):
        """
        Tests that DELETing entry/hazards/<id> deletes the item
        """
        response = self.client.delete(
            reverse('edit-hazard', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Hazard.DoesNotExist):
            Hazard.objects.get(id=2)

        response = self.client.delete(
            reverse('edit-hazard', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 404)
