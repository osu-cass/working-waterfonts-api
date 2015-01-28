from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import json


class POIsCategoriesTestCase(TestCase):
    fixtures = ['test_fixtures']

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
    }
  ]
}"""

        self.limited_pois_error = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  }
}"""

    def test_url_endpoint(self):
        url = reverse('pois-categories', kwargs={'id': '1'})
        self.assertEqual(url, '/1/pois/categories/1')

    def test_no_location_parameter(self):
        response = self.client.get(
            reverse('pois-categories', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)
        self.assertEqual(parsed_answer, expected_answer)

    def test_limit_parameter(self):
        response = self.client.get(
            "%s?limit=1" % reverse(
                'pois-categories', kwargs={'id': '2'})
        ).content

        parsed_answer = json.loads(response)
        expected_error = json.loads(self.limited_pois_error)

        self.assertEqual(parsed_answer['error'], expected_error['error'])
        self.assertEqual(len(parsed_answer['pois']), 1)


class POIsCategoriesLocationTestCase(TestCase):

    """
    Test whether the /pois/categories/<id> view returns the correct results
    when given a coordinate to center on.

    This is an individual class to allow the use of different fixture sets.
    """
    fixtures = ['location_fixtures']

    # These tests are made assuming a proximity of 20. If this default value
    # is changed, then the tests would break without overriding it.
    @override_settings(DEFAULT_PROXIMITY='20')
    def setUp(self):

        self.maxDiff = None

        # No POIs. This is the return for location queries from
        # the middle of nowhere.
        self.expected_no_pois = """
{
  "error": {
    "debug": "",
    "status": true,
    "level": "Information",
    "text": "No PointsOfInterest found for category 1",
    "name": "No PointsOfInterest"
    },
  "pois": []
}"""

        # Nearby POIs for category 1.
        # This JSON contains the two halibut stores in Newport and Waldport,
        # but not Portland. This is the return for a good coordinates.
        self.expected_cat1 = """
{
  "error": {
    "level": null,
    "status": false,
    "name": null,
    "debug": null,
    "text": null
  },
  "pointsofinterest": [
  {
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "street": "146 SE Bay Blvd",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.050122,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "location_description": "Located on Bay Blvd in Newport",
  "id": 3,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Tuna",
  "phone": null,
  "lat": 44.631592,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Newport Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
},
{
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "street": "522 NW Spring St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.066166,
  "city": "Waldport",
  "zip": "97394",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "location_description": "Located on Spring St in Waldport",
  "id": 5,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Waldport Tuna",
  "phone": null,
  "lat": 44.427761,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Waldport Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
}]
}"""

        # Nearby pois for cat1, with 50 mile range.
        # This JSON contains the POIs in Newport, Waldport, and
        # Pacific City, but not Portland. This is the return for a good
        # coordinates.
        self.expected_cat1_extended = """
{
  "error": {
    "debug": null,
    "status": false,
    "text": null,
    "name": null,
    "level": null
  },
  "pointsofinterest": [
{
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "street": "146 SE Bay Blvd",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.050122,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "location_description": "Located on Bay Blvd in Newport",
  "id": 3,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Tuna",
  "phone": null,
  "lat": 44.631592,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Newport Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
},
{
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "street": "522 NW Spring St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.066166,
  "city": "Waldport",
  "zip": "97394",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "location_description": "Located on Spring St in Waldport",
  "id": 5,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Waldport Tuna",
  "phone": null,
  "lat": 44.427761,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Waldport Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
},
{
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "facts": "",
  "street": "35650 Roger Ave",
  "alt_name": "",
  "contact_name": "",
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "id": 7,
  "city": "Cloverdale",
  "zip": "97112",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "ext": {

  },
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Pacific City Tuna",
  "phone": null,
  "lat": 45.197105,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Pacific City Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "location_description": "Located on Roger Ave in Pacific City",
  "lng": -123.958093,
  "history": ""
}
  ]
}"""

        # Nearby POIs for Cat1
        # This JSON contains the two halibut stores in Newport and Waldport,
        # but not Portland. This is the return for a good coordinates.
        self.expected_cat1_bad_limit = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad Limit",
    "debug": "ValueError: invalid literal for int() with base 10: 'cat'",
    "text": "Invalid limit. Returning all results."
  },
  "pointsofinterest": [
  {
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "street": "146 SE Bay Blvd",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.050122,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "location_description": "Located on Bay Blvd in Newport",
  "id": 3,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Tuna",
  "phone": null,
  "lat": 44.631592,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Newport Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
},
{
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "street": "522 NW Spring St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.066166,
  "city": "Waldport",
  "zip": "97394",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "location_description": "Located on Spring St in Waldport",
  "id": 5,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Waldport Tuna",
  "phone": null,
  "lat": 44.427761,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Waldport Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
}]
}"""

        self.expected_cat1_limit_1 = """
{
  "error": {
    "level": null,
    "status": false,
    "name": null,
    "debug": null,
    "text": null
  },
  "pointsofinterest": [
  {
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "street": "146 SE Bay Blvd",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.050122,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "location_description": "Located on Bay Blvd in Newport",
  "id": 3,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Tuna",
  "phone": null,
  "lat": 44.631592,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Newport Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
}]
}"""

        # All POIs for Category 1
        # This JSON contains the POIs in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_all_pois_cat1 = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "text": "There was an error with the given coordinates \
not_a_latitude, not_a_longitude",
    "name": "Bad location",
    "debug": "ValueError: String or unicode input unrecognized \
as WKT EWKT, and HEXEWKB."
  },
  "pointsofinterest": [
  {
    "id": 1,
    "website": "",
    "street": "720 SW Broadway",
      "city": "Portland",
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "lng": -122.67963,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Tuna",
    "phone": null,
    "lat": 45.518962,
    "name": "Portland Tuna",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
  },
  {
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
      "city": "Newport",
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "lng": -124.050122,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
      "city": "Waldport",
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "lng": -124.066166,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
  },
    {
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "lng": -123.958093,
      "email": "",
            "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "lat": 45.197105,
          "id": 7,
      "name": "Pacific City Tuna",
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
    }
  ]
}"""

        # All POIs for category 1 This is the return for a bad proximity with
        # good location -- the default proximity of 20 miles.
        self.expected_cat1_bad_prox = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "text": "There was an error finding pois within cat miles",
    "name": "Bad proximity",
    "debug": "ValueError: invalid literal for int() with base 10: 'cat'"
  },
  "pointsofinterest": [
  {
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "street": "146 SE Bay Blvd",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.050122,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "location_description": "Located on Bay Blvd in Newport",
  "id": 3,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Tuna",
  "phone": null,
  "lat": 44.631592,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Newport Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
},
{
  "videos": [
    {
      "caption": "Traveling at the speed of light!",
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship"
    }
  ],
  "images": [
    {
      "caption": "Meow!",
      "link": "/media/cat.jpg",
      "name": "A cat"
    }
  ],
  "street": "522 NW Spring St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.066166,
  "city": "Waldport",
  "zip": "97394",
  "hazards": [
    {
      "id": 1,
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 3,
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead."
    },
    {
      "id": 5,
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead."
    }
  ],
  "location_description": "Located on Spring St in Waldport",
  "id": 5,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Waldport Tuna",
  "phone": null,
  "lat": 44.427761,
  "categories": [
    {
      "category": "Cool Stuff",
      "id": 1
    },
    {
      "category": "Fish Shops",
      "id": 3
    },
    {
      "category": "Large Obelisks",
      "id": 5
    }
  ],
  "name": "Waldport Tuna",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
}]
}"""

        # All POIs for category 1. This is the return for a bad coordinates.
        self.expected_all_missing_long = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad location",
    "text": "There was an error with the given coordinates -45.232, None",
    "debug": "GEOSException: Error encountered checking Geometry returned \
from GEOS C function \\"GEOSWKTReader_read_r\\"."
  },
  "pointsofinterest": [
  {
    "id": 1,
    "website": "",
    "street": "720 SW Broadway",
      "city": "Portland",
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "lng": -122.67963,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Tuna",
    "phone": null,
    "lat": 45.518962,
    "name": "Portland Tuna",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
  },
  {
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
      "city": "Newport",
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "lng": -124.050122,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
      "city": "Waldport",
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "lng": -124.066166,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
  },
    {
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "lng": -123.958093,
      "email": "",
            "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "lat": 45.197105,
          "id": 7,
      "name": "Pacific City Tuna",
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
    }
  ]
}"""

        # All POIs with cat1. This is the return for a bad coordinates.
        self.expected_all_missing_lat = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad location",
    "text": "There was an error with the given coordinates None, -45.232",
    "debug": "GEOSException: Error encountered checking Geometry \
returned from GEOS C function \\"GEOSWKTReader_read_r\\"."
  },
  "pointsofinterest": [
  {
    "id": 1,
    "website": "",
    "street": "720 SW Broadway",
      "city": "Portland",
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "lng": -122.67963,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Tuna",
    "phone": null,
    "lat": 45.518962,
    "name": "Portland Tuna",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
  },
  {
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
      "city": "Newport",
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "lng": -124.050122,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
      "city": "Waldport",
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "lng": -124.066166,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
  },
    {
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "lng": -123.958093,
      "email": "",
            "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "lat": 45.197105,
          "id": 7,
      "name": "Pacific City Tuna",
    "images": [{
      "link": "/media/cat.jpg",
      "caption": "Meow!",
      "name": "A cat"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=efgDdSWDg0g",
      "name": "A Starship",
      "caption": "Traveling at the speed of light!"}
    ],
    "categories": [
      {
        "category": "Cool Stuff",
        "id": 1
      },
      {
        "category": "Fish Shops",
        "id": 3
      },
      {
        "category": "Large Obelisks",
        "id": 5
      }
    ],
    "hazards": [
      {
      "name": "Falling Rocks",
      "description": "If these fall on you, you're dead.",
        "id": 1
      },
      {
      "name": "Falling Rocks 3",
      "description": "If these fall on you, you're dead.",
        "id": 3
      },
      {
      "name": "Falling Rocks 5",
      "description": "If these fall on you, you're dead.",
        "id": 5
      }
    ]
    }
  ]
}"""

    def test_no_pois_nearby_poi_categories(self):
        """
        Test that, when there are no pois, we get an empty list back for the
        pois/categories endpoint.
        """
        no_poi_data = json.loads(
            self.client.get(
                '%s?lat=44.015225&lng=-123.016873' % reverse(
                    'pois-categories', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_no_pois)
        self.assertEqual(no_poi_data, expected_answer)

    def test_successful_location_by_poi_category(self):
        """
        Test that good parameters return poi/category results ordered by
        location. There will also be a default limit of 20 miles.
        """
        response_cat1 = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538' % reverse('pois-categories',
                                                         kwargs={'id': '1'})
        ).content)

        expected_answer = json.loads(self.expected_cat1)
        self.assertEqual(response_cat1, expected_answer)

    def test_good_limit_by_poi_category(self):
        """
        Test that good parameters return poi/category results ordered by
        location. There will also be a default limit of 20 miles.
        """
        response_cat1_limit = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=1' % reverse(
                'pois-categories', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_cat1_limit_1)
        self.assertEqual(response_cat1_limit, expected_answer)

    def test_limit_larger_than_length_all_categories(self):
        """
        Test that a limit larger than the length of the list does not
        affect the list.
        """
        response_cat1 = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=10' % reverse(
                'pois-categories', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_cat1)
        self.assertEqual(response_cat1, expected_answer)

    def test_bad_limit_by_poi_category(self):
        """
        Test that good parameters return poi/category results ordered by
        location. There will also be a default limit of 20 miles.
        """
        response_cat1_limit = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=cat' % reverse(
                'pois-categories', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_cat1_bad_limit)
        self.assertEqual(response_cat1_limit, expected_answer)

    def test_bad_location_parameters_poi_categories(self):
        """
        Test that only one parameter (only lat/only long) returns a Warning,
        and that bad parameter values (text) return Warning, for the
        pois/categories endpoint.
        """

        # Coordinates are not numbers
        broken_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&lng=not_a_longitude' % reverse(
                'pois-categories', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_all_pois_cat1)
        self.assertEqual(broken_data, expected_answer)

        # lat is missing
        broken_data = json.loads(self.client.get(
            '%s?lng=-45.232' % reverse(
                'pois-categories', kwargs={'id': '1'})).content)
        expected_answer = json.loads(self.expected_all_missing_lat)

        self.assertEqual(broken_data, expected_answer)

        # long is missing
        broken_data = json.loads(self.client.get(
            '%s?lat=-45.232' % reverse(
                'pois-categories', kwargs={'id': '1'})).content)
        expected_answer = json.loads(self.expected_all_missing_long)

        self.assertEqual(broken_data, expected_answer)

    def test_successful_location_by_poi_category_extended_proximity(self):
        """
        Test that good parameters return poi/category results ordered by
        location, with an extended proximity of 50 miles. This will include
        the Pacific City location.
        """
        response_cat1_extended = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538'
            '&proximity=50' % reverse(
                'pois-categories', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_cat1_extended)
        self.assertEqual(response_cat1_extended, expected_answer)

    def test_proximity_bad_location_poi_categories(self):
        """
        Test that bad location returns a Warning.
        """
        # Good proximity, bad location
        broken_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&lng=not_a_longitude&proximity=50' % reverse(
                'pois-categories', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_all_pois_cat1)
        self.assertEqual(broken_data, expected_answer)

    def test_bad_proximity_good_location_poi_categories(self):
        """
        Test that bad proximity returns a Warning.
        """
        broken_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&proximity=cat' % reverse(
                'pois-categories', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_cat1_bad_prox)
        self.assertEqual(broken_data, expected_answer)
