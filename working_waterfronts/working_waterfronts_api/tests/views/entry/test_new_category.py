from django.test import TestCase
from django.core.urlresolvers import reverse
from working_waterfronts.working_waterfronts_api.models import Category
from django.contrib.auth.models import User, Group


class NewCategoryTestCase(TestCase):

    """
    Test that the New Category page works as expected.

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

        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        response = self.client.login(
            username='temporary', password='temporary')
        self.assertEqual(response, True)

    def test_url_endpoint(self):
        url = reverse('new-category')
        self.assertEqual(url, '/entry/categories/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('new-category'))

        fields = {'category': 'input'}
        form = response.context['category_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_category_creation(self):
        """
        POST a proper "new category" command to the server, and see if the
        new category appears in the database.
        """
        Category.objects.all().delete()

        # Data that we'll post to the server to get the new category created
        new_category = {
            'category': 'Friers'}

        self.client.post(reverse('new-category'), new_category)

        category = Category.objects.all()[0]
        for field in new_category:
            self.assertEqual(
                getattr(category, field), new_category[field])

    def test_no_data_error(self):
        """
        POST a "new category" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_categories = Category.objects.all()

        response = self.client.post(reverse('new-category'))
        required_fields = ['category']
        for field_name in required_fields:
            self.assertIn(field_name,
                          response.context['category_form'].errors)

        # Test that we didn't add any new objects
        self.assertEqual(
            list(Category.objects.all()), list(all_categories))
