from django.test import TestCase
from django.core.urlresolvers import reverse
from working_waterfronts.working_waterfronts_api.models import PointOfInterest, Story
from django.contrib.auth.models import User, Group


class EditPointOfInterestTestCase(TestCase):

    """
    Test that the Edit PointOfInterest page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the pointofinterest
            object with the specified ID
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
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
            reverse('edit-pointofinterest', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/pointofinterests/1')

    def test_url_endpoint(self):
        url = reverse('edit-pointofinterest', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/pointofinterests/1')

    def test_successful_pointofinterest_update(self):
        """
        POST a proper "new pointofinterest" command to the server, and see if the
        new pointofinterest appears in the database
        """

        # Data that we'll post to the server to get the new pointofinterest created
        new_pointofinterest = {
            'zip': '97365', 'website': '', 'hours': '',
            'street': '750 NW Lighthouse Dr', 'story': 1,
            'status': '', 'state': 'OR', 'preparation_ids': '1,2',
            'phone': '', 'name': 'Test Name',
            'location_description': 'Optional Description',
            'email': '', 'description': 'Test Description',
            'contact_name': 'Test Contact', 'city': 'Newport'}

        self.client.post(
            reverse('edit-pointofinterest', kwargs={'id': '1'}), new_pointofinterest)

        # These values are changed by the server after being received from
        # the client/web page. The preparation IDs are going to be changed
        # into pointofinterest_product objects, so we'll not need the preparations_id
        # field
        del new_pointofinterest['preparation_ids']
        new_pointofinterest['status'] = None
        new_pointofinterest['phone'] = None
        new_pointofinterest['story'] = Story.objects.get(id=new_pointofinterest['story'])

        vend = PointOfInterest.objects.get(id=1)
        for field in new_pointofinterest:
            self.assertEqual(getattr(vend, field), new_pointofinterest[field])

        self.assertEqual(vend.location.y, 44.6752643)  # latitude
        self.assertEqual(vend.location.x, -124.072162)  # longitude

        # We told it which product preparation ID to use by saving ProdPreps to
        # IDs 1 and 2, and then posting '1,2' as the list of product
        # preparations.
        product_preparations = ([
            vp.product_preparation.id for vp in vend.pointofinterestproduct_set.all()])

        self.assertEqual(sorted(product_preparations), [1, 2])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields with the
        right initial data
        """

        response = self.client.get(reverse('edit-pointofinterest', kwargs={'id': '1'}))

        fields = {
            "name": "No Optional Null Fields Are Null",
            "status": True,
            "description": "This is a pointofinterest shop.",
            "hours": "Open Tuesday, 10am to 5pm",
            "street": "1633 Sommerville Rd",
            "city": "Sausalito",
            "state": "CA",
            "zip": "94965",
            "location_description": "Location description",
            "contact_name": "A. Persson",
            "story": 1,
            "website": "http://example.com",
            "email": "a@perr.com"
        }

        phone = 5417377627

        form = response.context['pointofinterest_form']
        self.assertEqual(phone, form['phone'].value().national_number)

        for field in fields:
            self.assertEqual(fields[field], form[field].value())

    def test_delete_pointofinterest(self):
        """
        Tests that DELETing entry/pointofinterests/<id> deletes the item
        """
        response = self.client.delete(
            reverse('edit-pointofinterest', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(PointOfInterest.DoesNotExist):
            PointOfInterest.objects.get(id=2)

        response = self.client.delete(
            reverse('edit-pointofinterest', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 404)
