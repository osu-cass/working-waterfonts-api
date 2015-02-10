from django.test import TestCase
from django.core.urlresolvers import reverse
from working_waterfronts.working_waterfronts_api.models import Category
from django.contrib.auth.models import User


class EditCategoryTestCase(TestCase):

    """
    Test that the Edit Category page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the category
            object with the specified ID
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
        url = reverse('edit-category', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/categories/1')

    def test_successful_category_update(self):
        """
        POST a proper "update category" command to the server, and see if
        the update appears in the database
        """
        # Data that we'll post to the server to get the new category created
        new_category = {
            "category": "Alien Habitats"
        }

        self.client.post(
            reverse('edit-category', kwargs={'id': '1'}),
            new_category)

        category = Category.objects.get(id=1)
        for field in new_category:
            self.assertEqual(
                getattr(category, field), new_category[field])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(
            reverse('edit-category', kwargs={'id': '1'}))

        fields = {
            "category": "Cool Stuff"
        }

        form = response.context['category_form']

        for field in fields:
            self.assertEqual(fields[field], form[field].value())

    def test_delete_category(self):
        """
        Tests that DELETing entry/categories/<id> deletes the item
        """
        response = self.client.delete(
            reverse('edit-category', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=2)

        response = self.client.delete(
            reverse('edit-category', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 404)
