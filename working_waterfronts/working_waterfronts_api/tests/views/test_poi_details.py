from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import json


class POITestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(reverse('login'), {'username': 'test',
                                            'password': 'pass'})

        self.expected_poi = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  },
  "name": "No Optional Null Fields Are Null",
  "status": true,
  "description": "This is a poi shop.",
  "lat": 37.833688,
  "lng": -122.478002,
  "street": "1633 Sommerville Rd",
  "city": "Sausalito",
  "state": "CA",
  "zip": "94965",
  "hours": "Open Tuesday, 10am to 5pm",
  "location_description": "Location description",
  "contact_name": "A. Persson",
  "phone": "+15417377627",
  "website": "http://example.com",
  "email": "a@perr.com",
  "story": 1,
  "ext": {},
  "id": 1,
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "products": [
    {
      "product_id": 2,
      "preparation_id": 1,
      "name": "Starfish Voyager",
      "preparation": "Live"
    },
    {
      "product_id": 1,
      "preparation_id": 1,
      "name": "Ezri Dax",
      "preparation": "Live"
    }
  ]
}"""

        self.expected_not_found = """
{
  "error": {
    "status": true,
    "text": "POI id 999 was not found.",
    "name": "POI Not Found",
    "debug": "DoesNotExist: POI matching query does not exist.",
    "level": "Error"
  }
}"""

    def test_url_endpoint(self):
        url = reverse('poi-details', kwargs={'id': '1'})
        self.assertEqual(url, '/1/pois/1')

    def test_known_poi(self):
        response = self.client.get(
            reverse('poi-details', kwargs={'id': '1'})).content

        parsed_answer = json.loads(response)
        expected_answer = json.loads(self.expected_poi)

        self.maxDiff = None
        self.assertEqual(parsed_answer, expected_answer)

    def test_poi_not_found(self):
        response = self.client.get(
            reverse('poi-details', kwargs={'id': '999'}))
        self.assertEqual(response.status_code, 404)

        parsed_answer = json.loads(response.content)
        expected_answer = json.loads(self.expected_not_found)

        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)
