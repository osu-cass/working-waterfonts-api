import json
from django.test import TestCase
from working_waterfronts.working_waterfronts_api.models import (
    PointOfInterest, Hazard, Category)
from django.contrib.gis.geos import fromstr
from working_waterfronts.working_waterfronts_api.views.serializer import (
    FreshSerializer)


class SerializerTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        self.maxDiff = None
        self.expected_poi_json = """
[{
  "street": "123 Fake St",
  "alt_name": "",
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
  "contact_name": "",
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
  "name": "Newport Lighthouse",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "location_description": "out on the cape over there",
  "history": "It was built at some time in the past"
}]"""

        self.expected_hazard_json = """[
  {
    "name": "Falling Rocks",
    "created": "2014-08-08T23:27:05.568Z",
    "modified": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "id": 1,
    "description": "If these fall on you, you're dead."
  }
]"""

        self.expected_category_json = """[
  {
    "category": "Cool Stuff",
    "ext": {

    },
    "id": 1,
    "modified": "2014-08-08T23:27:05.568Z",
    "created": "2014-08-08T23:27:05.568Z"
  }
]"""

    def test_serializer_poi(self):
        serializer = FreshSerializer()
        data = serializer.serialize(
                [PointOfInterest.objects.get(id=1)],
                use_natural_foreign_keys=True
            )

        parsed_answer = json.loads(data)
        expected_answer = json.loads(self.expected_poi_json)

        self.assertEqual(parsed_answer, expected_answer)

    def test_serializer_hazard(self):
        serializer = FreshSerializer()
        data = serializer.serialize(
                [Hazard.objects.get(id=1)],
                use_natural_foreign_keys=True
            )

        parsed_answer = json.loads(data)
        expected_answer = json.loads(self.expected_hazard_json)

        self.assertEqual(parsed_answer, expected_answer)

    def test_serializer_category(self):
        serializer = FreshSerializer()
        data = serializer.serialize(
                [Category.objects.get(id=1)],
                use_natural_foreign_keys=True
            )

        parsed_answer = json.loads(data)
        expected_answer = json.loads(self.expected_category_json)

        self.assertEqual(parsed_answer, expected_answer)