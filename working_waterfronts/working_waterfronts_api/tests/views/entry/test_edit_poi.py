from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from working_waterfronts.working_waterfronts_api.models import PointOfInterest


class EditPointOfInterestTestCase(TestCase):

    """
    Test that the Edit PointOfInterest page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the poi
            object with the specified ID
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
    """
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        response = self.client.login(
            username='temporary', password='temporary')
        self.assertEqual(response, True)

    def test_url_endpoint(self):
        url = reverse('edit-poi', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/pois/1')

    def test_successful_poi_update(self):
        """
        POST a proper "new poi" command to the server, and see if the
        new poi appears in the database
        """

        # Data that we'll post to the server to get the poi updated
        new_poi = {
            'name': 'Test Name', 'alt_name': 'Tester Obj',
            'description': 'Test Description',
            'history': 'history', 'facts': 'It\'s a test',
            'street': '750 NW Lighthouse Dr', 'city': 'Newport', 'state': 'OR',
            'zip': '97365', 'location_description': 'test loc description',
            'contact_name': 'Test Contact', 'website': '', 'email': '',
            'phone': '', 'category_ids': '1,2', 'hazard_ids': '1,2',
            'image_ids': '', 'video_ids': ''}

        self.client.post(
            reverse('edit-poi', kwargs={'id': '1'}), new_poi)

        # These values are changed by the server after being received from
        # the client/web page. The preparation IDs are going to be changed
        # into objects, so we'll not need the list fields
        del new_poi['category_ids']
        del new_poi['hazard_ids']
        del new_poi['video_ids']
        del new_poi['image_ids']
        new_poi['phone'] = None

        poi = PointOfInterest.objects.get(id=1)
        for field in new_poi:
            self.assertEqual(getattr(poi, field), new_poi[field])

        self.assertEqual(poi.location.y, 44.6752643)  # latitude
        self.assertEqual(poi.location.x, -124.072162)  # longitude

        hazards = [hazard.id for hazard in poi.hazards.all()]
        categories = [category.id for category in poi.categories.all()]

        self.assertEqual(sorted(hazards), [1, 2])
        self.assertEqual(sorted(categories), [1, 2])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields with the
        right initial data
        """

        response = self.client.get(reverse('edit-poi', kwargs={'id': '1'}))

        fields = {
            "name": "Newport Lighthouse",
            "alt_name": "",
            "description": "A pretty nice lighthouse",
            "history": "It was built at some time in the past",
            "facts": "It's a lighthouse",
            "street": "123 Fake St",
            "city": "Newport",
            "state": "Oregon",
            "location_description": "out on the cape over there",
            "zip": "11234",
            "website": "",
            "email": "",
            "phone": None,
        }

        form = response.context['poi_form']

        for field in fields:
            self.assertEqual(fields[field], form[field].value())

    def test_delete_poi(self):
        """
        Tests that DELETing entry/pois/<id> deletes the item
        """
        response = self.client.delete(
            reverse('edit-poi', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(PointOfInterest.DoesNotExist):
            PointOfInterest.objects.get(id=2)

        response = self.client.delete(
            reverse('edit-poi', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 404)
