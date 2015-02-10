from django.test import TestCase
from django.core.urlresolvers import reverse
from working_waterfronts.working_waterfronts_api.models import Hazard
from django.contrib.auth.models import User


class NewHazardTestCase(TestCase):

    """
    Test that the New Hazard page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the creation of a new
            object with the specified details
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
    """

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        response = self.client.login(
            username='temporary', password='temporary')
        self.assertEqual(response, True)

    def test_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse('new-hazard'))
        self.assertRedirects(response, '/login?next=/entry/hazards/new')

    def test_url_endpoint(self):
        url = reverse('new-hazard')
        self.assertEqual(url, '/entry/hazards/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('new-hazard'))

        fields = {'name': 'input', 'description': 'textarea'}
        form = response.context['hazard_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_hazard_creation_minimal(self):
        """
        POST a proper "new hazard" command to the server, and see if the
        new hazard appears in the database. All optional fields are null.
        """
        Hazard.objects.all().delete()

        # Data that we'll post to the server to get the new hazard created
        new_hazard = {
            'name': 'Frier', 'description': 'Some Text'}

        self.client.post(reverse('new-hazard'), new_hazard)

        hazard = Hazard.objects.all()[0]
        for field in new_hazard:
            self.assertEqual(
                getattr(hazard, field), new_hazard[field])

    def test_successful_hazard_creation_maximal(self):
        """
        POST a proper "new hazard" command to the server, and see if the
        new hazard appears in the database. All optional fields are used.
        """
        Hazard.objects.all().delete()

        # Data that we'll post to the server to get the new hazard created
        new_hazard = {
            'name': 'Frier',
            'description': "You'll be fried"
        }

        self.client.post(reverse('new-hazard'), new_hazard)

        hazard = Hazard.objects.all()[0]
        for field in new_hazard:
            self.assertEqual(
                getattr(hazard, field), new_hazard[field])

    def test_no_data_error(self):
        """
        POST a "new hazard" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_hazards = Hazard.objects.all()

        response = self.client.post(reverse('new-hazard'))
        required_fields = ['name']
        for field_name in required_fields:
            self.assertIn(field_name,
                          response.context['hazard_form'].errors)

        # Test that we didn't add any new objects
        self.assertEqual(
            list(Hazard.objects.all()), list(all_hazards))
