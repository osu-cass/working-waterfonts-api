from django.test import TestCase
from django.core.urlresolvers import reverse
from working_waterfronts.working_waterfronts_api.models import (
    PointOfInterest, Category, Hazard)


class NewPOITestCase(TestCase):

    """
    Test that the New POI page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the creation of a new
            object with the specified details
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
        POSTing a valid object with a bad address returns an error saying
            bad adddress. This behaviour may be changed in the future.
    """

    def test_url_endpoint(self):
        url = reverse('new-poi')
        self.assertEqual(url, '/entry/pois/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('new-poi'))

        fields = {
            'name': 'input', 'alt_name': 'input', 'description': 'textarea',
            'history': 'textarea', 'facts': 'textarea',
            'street': 'input', 'city': 'input', 'state': 'input',
            'zip': 'input', 'location_description': 'textarea',
            'contact_name': 'input', 'website': 'input', 'email': 'input',
            'phone': 'input'}
        form = response.context['poi_form']

        for field in fields:
            self.assertIn(fields[field], str(form[field]))

    def test_successful_pointofinterest_creation(self):
        """
        POST a proper "new pointofinterest" command to the server, and see if
        the new pointofinterest appears in the database
        """
        # Create objects that we'll be setting as the foreign objects for
        # our test POI
        Hazard.objects.all().delete()
        Category.objects.all().delete()

        Hazard.objects.create(id=1)
        Hazard.objects.create(id=2)
        Category.objects.create(id=1)
        Category.objects.create(id=2)

        # Data that we'll post to the server to get the new poi created
        new_poi = {
            'name': 'Test Name', 'alt_name': 'Tester Obj',
            'description': 'Test Description',
            'history': 'history', 'facts': 'It\'s a test',
            'street': '750 NW Lighthouse Dr', 'city': 'Newport', 'state': 'OR',
            'zip': '97365', 'location_description': 'test loc description',
            'contact_name': 'Test Contact', 'website': '', 'email': '',
            'phone': '', 'category_ids': '1,2', 'hazard_ids': '1,2'}

        self.client.post(reverse('new-poi'), new_poi)

        self.assertGreater(len(PointOfInterest.objects.all()), 0)

        # These values are changed by the server after being received from
        # the client/web page. The preparation IDs are going to be changed
        # into objects, so we'll not need the list fields
        del new_poi['category_ids']
        del new_poi['hazard_ids']
        new_poi['phone'] = None

        poi = PointOfInterest.objects.all()[0]
        for field in new_poi:
            self.assertEqual(getattr(poi, field), new_poi[field])

        self.assertEqual(poi.location.y, 44.6752643)  # latitude
        self.assertEqual(poi.location.x, -124.072162)  # longitude

        hazards = [hazard.id for hazard in poi.hazards.all()]
        categories = [category.id for category in poi.categories.all()]

        self.assertEqual(sorted(hazards), [1, 2])
        self.assertEqual(sorted(categories), [1, 2])

    def test_no_data_error(self):
        """
        POST a "new pointofinterest" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_pointsofinterest = PointOfInterest.objects.all()

        new_poi = {
            'name': '', 'alt_name': '', 'description': '',
            'history': '', 'facts': '',
            'street': '', 'city': '', 'state': '',
            'zip': '', 'location_description': '',
            'contact_name': '', 'website': '', 'email': '',
            'phone': '', 'category_ids': '', 'hazard_ids': ''}

        response = self.client.post(reverse('new-poi'), new_poi)

        # Test non-automatically generated errors written into the view
        self.assertIn('Full address is required.', response.context['errors'])
        self.assertIn(
            'You must choose at least one category.',
            response.context['errors'])
        # Test that we didn't add any new objects
        self.assertEqual(
            list(PointOfInterest.objects.all()),
            list(all_pointsofinterest))

    def test_bad_address(self):
        """
        POST a "new pointofinterest" to the server with a bad address --
        a non-existant street -- and test that a Bad Address error is returned.

        This test contains the same POST data as the
        test_successful_pointofinterest_creation, but with a bad address.
        This means the only error returned should be a Bad Address error.
        """

        all_pointsofinterest = PointOfInterest.objects.all()

        Hazard.objects.all().delete()
        Category.objects.all().delete()

        Hazard.objects.create(id=1)
        Hazard.objects.create(id=2)
        Category.objects.create(id=1)
        Category.objects.create(id=2)

        # Data that we'll post to the server to get the new poi created
        new_poi = {
            'name': 'Test Name', 'alt_name': 'Tester Obj',
            'description': 'Test Description',
            'history': 'history', 'facts': 'It\'s a test',
            'street': '123 Fake Street', 'city': 'Springfield', 'state': 'OR',
            'zip': '97477', 'location_description': 'test loc description',
            'contact_name': 'Test Contact', 'website': '', 'email': '',
            'phone': '', 'category_ids': '1,2', 'hazard_ids': '1,2'}

        response = self.client.post(reverse('new-poi'), new_poi)

        # Test that the bad address returns a bad address
        self.assertIn("Full address is required.", response.context['errors'])

        # Test that we didn't add any new objects
        self.assertEqual(
            list(PointOfInterest.objects.all()),
            list(all_pointsofinterest))
