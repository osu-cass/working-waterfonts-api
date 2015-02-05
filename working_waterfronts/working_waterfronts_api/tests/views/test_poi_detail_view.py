from django.test import TestCase
from django.core.urlresolvers import reverse

import json


class POIViewTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        self.expected_poi = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  },
  "street": "123 Fake St",
  "alt_name": "",
  "contact_name": "",
  "facts": "It's a lighthouse",
  "lng": -124.10534,
  "id": 1,
  "city": "Newport",
  "zip": "11234",
  "hazards": [
      {
          "name": "Falling Rocks",
          "description": "If these fall on you, you're dead.",
          "id": 1
      }
  ],
  "ext": {
  },
  "state": "Oregon",
  "email": "",
  "website": "",
  "description": "A pretty nice lighthouse",
  "phone": null,
  "lat": 43.966874,
  "categories": [
      {
          "category": "Cool Stuff",
          "id": 1
      }
  ],
  "videos": [
      {
          "caption": "Traveling at the speed of light!",
          "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
          "name": "A Starship"
      }
  ],
  "images": [
      {
          "caption": "Woof!",
          "link": "/media/dog.jpg",
          "name": "A dog"
      }
  ],
  "name": "Newport Lighthouse",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "location_description": "out on the cape over there",
  "history": "It was built at some time in the past"
}"""

        self.expected_not_found = """
{
  "error": {
    "status": true,
    "text": "poi id 999 was not found.",
    "name": "poi Not Found",
    "debug": "UnboundLocalError: local variable 'poi' referenced before \
assignment",
    "level": "Error"
  }
}"""

    def test_url_endpoint(self):
        url = reverse('poi-details', kwargs={'id': '1'})
        self.assertEqual(url, '/1/pois/1')

    def test_known_poi(self):
        response = self.client.get(
            reverse('poi-details', kwargs={'id': '1'}))

        parsed_answer = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        expected_answer = json.loads(self.expected_poi)
        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)

    def test_poi_not_found(self):
        response = self.client.get(
            reverse('poi-details', kwargs={'id': '999'}))
        parsed_answer = json.loads(response.content)
        self.assertEqual(response.status_code, 404)

        expected_answer = json.loads(self.expected_not_found)
        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)
