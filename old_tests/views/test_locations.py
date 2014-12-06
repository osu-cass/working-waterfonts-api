from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class LocationsTestCase(TestCase):
    fixtures = ["real_data"]

    def setUp(self):
        self.maxDiff = None
        self.expected_json = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  },
  "locations": [
    {
      "location": 0,
      "name": "Gold Beach"
    },
    {
      "location": 1,
      "name": "Corvallis"
    },
    {
      "location": 2,
      "name": "Florence"
    },
    {
      "location": 3,
      "name": "Newport"
    },
    {
      "location": 4,
      "name": "Waldport"
    }
  ]
}"""

    def test_url_endpoint(self):
        url = reverse("locations")
        self.assertEqual(url, '/1/locations')

    def test_location_list(self):
        response = self.client.get('/1/locations').content
        try:
            parsed_answer = json.loads(response)
        except ValueError:
            self.fail("Received answer is not JSON")

        expected_answer = json.loads(self.expected_json)
        self.assertEqual(parsed_answer, expected_answer)
