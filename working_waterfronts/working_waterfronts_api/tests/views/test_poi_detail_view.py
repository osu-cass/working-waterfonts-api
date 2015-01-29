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
   "pointsofinterest": [
        {
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
        },
        {
            "name": "Haystack Rock",
            "alt_name": "",
            "contact_name": "",
            "description": "A pretty nice rock",
            "history": "Nature made it",
            "facts": "It's a nature habitat place, no climbing!",
            "street": "123 Fake St",
            "city": "Canon Beach",
            "state": "Oregon",
            "location_description": "",
            "zip": "11234",
            "website": "http://hatstackrock.com",
            "email": "rock@haystackrock.com",
            "phone": "+1 555 123 4567",
            "created": "2014-08-08T23:27:05.568Z",
            "modified": "2014-08-08T23:27:05.568Z",
            "lng": -124.10534,
            "id": 2,
            "ext": {
            },
            "lat": 43.966874,
            "hazards": [
                {
                    "name": "Alien Abduction",
                    "description": "This site is liable to result \
                    in you being abducted by aliens.",
                    "id": 2
                }
            ],
            "categories": [
                {
                    "category": "Uncool Stuff",
                    "id": 2
                }
            ],
            "videos": [
                {
                    "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
                    "caption": "Princely",
                    "name": "Princely"
                }
            ],
            "images": [
                {
                    "link": "/media/cat.jpg",
                    "caption": "Meow!",
                    "name": "A cat"
                }
            ]
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
