from django.test import TestCase
from django.core.urlresolvers import reverse
from working_waterfronts.working_waterfronts_api.models import (PointOfInterest, ProductPreparation,
                                                Product, Preparation, Story)
from django.contrib.auth.models import User, Group


class NewPointOfInterestTestCase(TestCase):

    """
    Test that the New PointOfInterest page works as expected.

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
        url = reverse('new-pointofinterest')
        self.assertEqual(url, '/entry/pointofinterests/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.post(
            reverse('login'),
            {'username': 'temporary', 'password': 'temporary'})
        response = self.client.get(reverse('new-pointofinterest'))

        fields = {'name': 'input', 'description': 'textarea', 'hours': 'input',
                  'story': 'select', 'status': 'select', 'street': 'input',
                  'city': 'input', 'state': 'input', 'zip': 'input',
                  'location_description': 'textarea', 'contact_name': 'input',
                  'website': 'input', 'email': 'input', 'phone': 'input'}
        form = response.context['pointofinterest_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_pointofinterest_creation(self):
        """
        POST a proper "new pointofinterest" command to the server, and see if the
        new pointofinterest appears in the database
        """
        self.client.post(reverse('login'),
                         {'username': 'temporary', 'password': 'temporary'})
        # Create objects that we'll be setting as the foreign objects for
        # our test pointofinterest

        # We'll want multiple product_preparations to
        # allow us to test the multi-product logic.

        # We can't predict what the ID of the new pointofinterest will be, so we can
        # delete all of the pointofinterests, and then choose the only pointofinterest left
        # after creation.
        PointOfInterest.objects.all().delete()

        Story.objects.create(id=1)
        product = Product.objects.create(id=1)
        preparation = Preparation.objects.create(id=1)

        ProductPreparation.objects.create(
            id=1, product=product, preparation=preparation)
        ProductPreparation.objects.create(
            id=2, product=product, preparation=preparation)

        # Data that we'll post to the server to get the new pointofinterest created
        new_pointofinterest = {
            'zip': '97365', 'website': '', 'hours': 'optional hours',
            'street': '750 NW Lighthouse Dr', 'story': '',
            'status': '', 'state': 'OR', 'preparation_ids': '1,2',
            'phone': '', 'name': 'Test Name',
            'location_description': 'Optional Description',
            'email': '', 'description': 'Test Description',
            'contact_name': 'Test Contact', 'city': 'Newport'}

        self.client.post(reverse('new-pointofinterest'), new_pointofinterest)

        self.assertGreater(len(PointOfInterest.objects.all()), 0)

        # These values are changed by the server after being received from
        # the client/web page. The preparation IDs are going to be changed
        # into pointofinterest_product objects, so we'll not need the preparations_id
        # field
        del new_pointofinterest['preparation_ids']
        new_pointofinterest['status'] = None
        new_pointofinterest['phone'] = None
        new_pointofinterest['story'] = None

        vend = PointOfInterest.objects.all()[0]
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

    def test_no_data_error(self):
        """
        POST a "new pointofinterest" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        response = self.client.post(
            reverse('login'),
            {'username': 'temporary', 'password': 'temporary'})
        # Create a list of all objects before sending bad POST data
        all_pointofinterests = PointOfInterest.objects.all()

        new_pointofinterest = {
            'zip': '', 'website': '', 'street': '', 'story': '',
            'status': '', 'state': '', 'preparation_ids': '',
            'phone': '', 'name': '', 'location_description': '',
            'email': '', 'description': '', 'contact_name': '',
            'city': '', 'hours': ''}

        response = self.client.post(reverse('new-pointofinterest'), new_pointofinterest)

        # Test non-automatically generated errors written into the view
        self.assertIn(
            'You must choose at least one product.',
            response.context['errors'])
        self.assertIn('Full address is required.', response.context['errors'])

        required_fields = [
            'city', 'name', 'zip', 'location', 'state',
            'street', 'contact_name', 'description']
        for field_name in required_fields:
            self.assertIn(field_name, response.context['pointofinterest_form'].errors)

        # Test that we didn't add any new objects
        self.assertTrue(list(PointOfInterest.objects.all()) == list(all_pointofinterests))

    def test_bad_address(self):
        """
        POST a "new pointofinterest" to the server with a bad address -- a non-existant
        street -- and test that a Bad Address error is returned.

        This test contains the same POST data as the
        test_successful_pointofinterest_creation, but with a bad address. This means
        the only error returned should be a Bad Address error.
        """
        response = self.client.post(
            reverse('login'),
            {'username': 'temporary', 'password': 'temporary'})
        # Create a list of all objects before sending bad POST data
        all_pointofinterests = PointOfInterest.objects.all()

        # Create objects that we'll be setting as the foreign objects for
        # our test pointofinterest

        # It needs a story, and we'll want multiple product_preparations to
        # allow us to test the multi-product logic.
        Story.objects.create(id=1)
        product = Product.objects.create(id=1)
        preparation = Preparation.objects.create(id=1)

        ProductPreparation.objects.create(
            id=1, product=product, preparation=preparation)
        ProductPreparation.objects.create(
            id=2, product=product, preparation=preparation)

        # Data that we'll post to the server to get the new pointofinterest created
        new_pointofinterest = {
            'zip': '97477', 'website': '', 'hours': '',
            'street': '123 Fake Street', 'story': 1,
            'status': '', 'state': 'OR', 'preparation_ids': '1,2',
            'phone': '', 'name': 'Test Name',
            'location_description': 'Optional Description',
            'email': '', 'description': 'Test Description',
            'contact_name': 'Test Contact', 'city': 'Springfield'}

        response = self.client.post(reverse('new-pointofinterest'), new_pointofinterest)

        # Test that the bad address returns a bad address
        self.assertIn("Full address is required.", response.context['errors'])

        # Test that we didn't add any new objects
        self.assertTrue(list(PointOfInterest.objects.all()) == list(all_pointofinterests))
