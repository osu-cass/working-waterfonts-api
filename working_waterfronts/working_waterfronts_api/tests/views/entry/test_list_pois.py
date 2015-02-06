from django.test import TestCase
from django.core.urlresolvers import reverse
from working_waterfronts.working_waterfronts_api.models import PointOfInterest


class ListPointOfInterestTestCase(TestCase):
    fixtures = ['thirtythree']

    def test_url_endpoint(self):
        url = reverse('entry-list-pois')
        self.assertEqual(url, '/entry/pois')

    def test_list_items(self):
        """
        Tests to see if the list of pois contains the proper
        pois and proper pointofinterest data
        """

        page_1 = self.client.get(reverse('entry-list-pois')).context
        page_2 = self.client.get(
            '{}?page=2'.format(reverse('entry-list-pois'))).context
        page_3 = self.client.get(
            '{}?page=3'.format(reverse('entry-list-pois'))).context
        page_4 = self.client.get(
            '{}?page=4'.format(reverse('entry-list-pois'))).context
        page_nan = self.client.get(
            '{}?page=NaN'.format(reverse('entry-list-pois'))).context

        self.assertEqual(
            list(page_1['item_list']),
            list(PointOfInterest.objects.order_by('name')[:15]))

        self.assertEqual(
            list(page_2['item_list']),
            list(PointOfInterest.objects.order_by('name')[15:30]))

        self.assertEqual(
            list(page_3['item_list']),
            list(PointOfInterest.objects.order_by('name')[30:33]))

        # Page 4 should be identical to Page 3, as these fixtures
        # have enough content for three pages (15 items per page, 33 items)

        self.assertEqual(
            list(page_3['item_list']),
            list(page_4['item_list']))

        # Page NaN should be identical to Page 1, as Django paginator returns
        # the first page if the page is not an int

        self.assertEqual(
            list(page_1['item_list']),
            list(page_nan['item_list']))
