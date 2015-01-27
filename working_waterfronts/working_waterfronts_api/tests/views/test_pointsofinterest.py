import json

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.contrib.auth.models import Group, User


class PointsOfInterestTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):

        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        self.maxDiff = None
        self.expected_list = """
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
            "description": "This site is liable to result in you being abducted by aliens.",
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
  }
"""

        self.expected_limited_error = """
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
        url = reverse('pois-list')
        self.assertEqual(url, '/1/pois')

    def test_no_parameters(self):
        Client()
        response = self.client.get(reverse('pois-list')).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_list)

        self.maxDiff = None
        self.assertEqual(parsed_answer, expected_answer)

    def test_limited_pointsofinterest(self):
        response = self.client.get(
            "%s?limit=1" % reverse('pois-list')).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_limited_error)

        self.assertEqual(parsed_answer['error'], expected_answer['error'])
        self.assertEqual(len(parsed_answer['pointsofinterest']), 1)


class NoPointOfInterestViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        self.expected_no_pointsofinterest = """
{
  "error": {
    "status": true,
    "text": "No PointsOfInterest found",
    "name": "No PointsOfInterest",
    "debug": "",
    "level": "Information"
  },
  "pointsofinterest": []
}"""

    def test_no_products(self):
        response = self.client.get(reverse('pois-list'))

        parsed_answer = json.loads(response.content)
        expected_answer = json.loads(self.expected_no_pointsofinterest)
        self.assertEqual(response.status_code, 200)

        expected_answer = json.loads(self.expected_no_pointsofinterest)

        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)


class PointsOfInterestLocationTestCase(TestCase):

    """
    Test whether the /pois/ view returns the correct results when given a
    coordinate to center on.

    For future test-writers: the location_fixtures tests have six pointsofinterest
    in them -- two in Newport, two in Waldport, and two in Portland. Each
    vendor has one product, and each product is sold at one of the two pointsofinterest
    in the city.

    This means you can easily test the proximity limit by limiting yourself
    to one city, or just the coast, etc.
    """
    fixtures = ['location_fixtures']

    # These tests are made assuming a proximity of 20. If this default value
    # is changed, then the tests would break without overriding it.
    @override_settings(DEFAULT_PROXIMITY='20')
    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        self.maxDiff = None

        # No pointsofinterest. This is the return for location queries from
        # the middle of nowhere.
        self.expected_no_pointsofinterest = """
{
  "error": {
            "debug": "",
            "status": true,
            "level": "Information",
            "text": "No PointsOfInterest found",
            "name": "No PointsOfInterest"
  },
  "pointsofinterest": []
}"""

        # All POIs around Newport
        # This JSON contains the four POIs in Newport and Waldport,
        # but not the Portland ones.
        self.expected_nearby_all_pointsofinterest = """
{
  "error": {
    "level": null,
    "status": false,
    "name": null,
    "debug": null,
    "text": null
  },
  "pointsofinterest": [{
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "1226 Oregon Coast Hwy",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.052868,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on Oregon Coast Hwy in Newport",
  "id": 4,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Halibut",
  "phone": null,
  "lat": 44.646006,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Newport Halibut",
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "190 SW Maple St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.069126,
  "city": "Waldport",
  "zip": "97364",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on SW Maple St in Waldport",
  "id": 6,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Waldport Halibut",
  "phone": null,
  "lat": 44.425188,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Waldport Halibut",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
}]
}"""

        # All POIs around Newport, with extended proximity.
        # This JSON contains the six POIs in Newport, Waldport, Pacific City
        # but not the Portland ones.
        self.expected_nearby_extended = """
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "1226 Oregon Coast Hwy",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.052868,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on Oregon Coast Hwy in Newport",
  "id": 4,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Halibut",
  "phone": null,
  "lat": 44.646006,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Newport Halibut",
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "190 SW Maple St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.069126,
  "city": "Waldport",
  "zip": "97364",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on SW Maple St in Waldport",
  "id": 6,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Waldport Halibut",
  "phone": null,
  "lat": 44.425188,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Waldport Halibut",
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
},
{
  "videos": [
    {
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "facts": "",
  "street": "34455 Brooten Rd",
  "alt_name": "",
  "contact_name": "",
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "id": 8,
  "city": "Cloverdale",
  "zip": "97112",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "ext": {

  },
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Pacific City Halibut",
  "phone": null,
  "lat": 45.207253,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Pacific City Halibut",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "location_description": "Located on Brooten Rd in Pacific City",
  "lng": -123.959418,
  "history": ""
}
  ]
}"""

        # All pointsofinterest for all products
        # This JSON contains the six fish stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_error_result = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "text": "There was an error with the given coordinates \
not_a_latitude, not_a_longitude",
    "name": "Bad location",
    "debug": "ValueError: String or unicode input unrecognized as \
WKT EWKT, and HEXEWKB."
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
    "id": 2,
    "website": "",
    "street": "1 SW Pine St",
      "city": "Portland",
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "lng": -122.670619,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Halibut",
    "phone": null,
    "lat": 45.520988,
    "name": "Portland Halibut",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/dog.jpg",
      "caption": "Woof!",
      "name": "A dog"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "caption": "Princely",
      "name": "Princely"}
    ],
    "categories": [
      {
        "category": "Uncool Stuff",
        "id": 2
      },
      {
        "category": "Non-Fish Shops",
        "id": 4
      },
      {
        "category": "Test Category Do Not Upvote",
        "id": 6
      }
    ],
    "hazards": [
      {
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 2
      },
      {
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 4
      },
      {
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 6
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
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
      "city": "Newport",
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "lng": -124.052868,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/dog.jpg",
      "caption": "Woof!",
      "name": "A dog"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "caption": "Princely",
      "name": "Princely"}
    ],
    "categories": [
      {
        "category": "Uncool Stuff",
        "id": 2
      },
      {
        "category": "Non-Fish Shops",
        "id": 4
      },
      {
        "category": "Test Category Do Not Upvote",
        "id": 6
      }
    ],
    "hazards": [
      {
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 2
      },
      {
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 4
      },
      {
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 6
      }
    ]
  },
  {
    "id": 6,
    "website": "",
    "street": "190 SW Maple St",
      "city": "Waldport",
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "lng": -124.069126,
    "state": "OR",
    "email": "",
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
    "ext": {

    },
    "images": [{
      "link": "/media/dog.jpg",
      "caption": "Woof!",
      "name": "A dog"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "caption": "Princely",
      "name": "Princely"}
    ],
    "categories": [
      {
        "category": "Uncool Stuff",
        "id": 2
      },
      {
        "category": "Non-Fish Shops",
        "id": 4
      },
      {
        "category": "Test Category Do Not Upvote",
        "id": 6
      }
    ],
    "hazards": [
      {
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 2
      },
      {
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 4
      },
      {
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 6
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
    },
    {
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Halibut",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "alt_name": "",
  "contact_name": "",
      "history": "",
      "facts": "",
      "ext": {

      },
      "location_description": "Located on Brooten Rd in Pacific City",
      "lng": -123.959418,
      "email": "",
            "phone": null,
      "state": "OR",
      "street": "34455 Brooten Rd",
      "lat": 45.207253,
          "id": 8,
      "name": "Pacific City Halibut",
    "images": [{
      "link": "/media/dog.jpg",
      "caption": "Woof!",
      "name": "A dog"}],
    "videos": [{
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "caption": "Princely",
      "name": "Princely"}
    ],
    "categories": [
      {
        "category": "Uncool Stuff",
        "id": 2
      },
      {
        "category": "Non-Fish Shops",
        "id": 4
      },
      {
        "category": "Test Category Do Not Upvote",
        "id": 6
      }
    ],
    "hazards": [
      {
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 2
      },
      {
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 4
      },
      {
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens.",
        "id": 6
      }
    ]
    }
  ]
}"""

        # All pointsofinterest for all products
        # This JSON contains the six fish stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_error_missing_long = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad location",
    "text": "There was an error with the given coordinates -45.232, None",
    "debug": "GEOSException: Error encountered checking \
Geometry returned from GEOS C function \\"GEOSWKTReader_read_r\\"."
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
  "street": "720 SW Broadway",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -122.67963,
  "city": "Portland",
  "zip": "97204",
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
  "location_description": "Located on Broadway in Portland",
  "id": 1,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Portland Tuna",
  "phone": null,
  "lat": 45.518962,
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
  "name": "Portland Tuna",
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "1 SW Pine St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -122.670619,
  "city": "Portland",
  "zip": "97204",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on Pine in Portland",
  "id": 2,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Portland Halibut",
  "phone": null,
  "lat": 45.520988,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Portland Halibut",
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "1226 Oregon Coast Hwy",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.052868,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on Oregon Coast Hwy in Newport",
  "id": 4,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Halibut",
  "phone": null,
  "lat": 44.646006,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Newport Halibut",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
},
{
  "videos": [
    {
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "190 SW Maple St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.069126,
  "city": "Waldport",
  "zip": "97364",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on SW Maple St in Waldport",
  "id": 6,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Waldport Halibut",
  "phone": null,
  "lat": 44.425188,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Waldport Halibut",
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
},
{
  "videos": [
    {
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "facts": "",
  "street": "34455 Brooten Rd",
  "alt_name": "",
  "contact_name": "",
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "id": 8,
  "city": "Cloverdale",
  "zip": "97112",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "ext": {

  },
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Pacific City Halibut",
  "phone": null,
  "lat": 45.207253,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Pacific City Halibut",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "location_description": "Located on Brooten Rd in Pacific City",
  "lng": -123.959418,
  "history": ""
}
  ]
}"""

        # All pointsofinterest for all products
        # This JSON contains the six fish stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_error_missing_lat = """
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
  "street": "720 SW Broadway",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -122.67963,
  "city": "Portland",
  "zip": "97204",
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
  "location_description": "Located on Broadway in Portland",
  "id": 1,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Portland Tuna",
  "phone": null,
  "lat": 45.518962,
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
  "name": "Portland Tuna",
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "1 SW Pine St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -122.670619,
  "city": "Portland",
  "zip": "97204",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on Pine in Portland",
  "id": 2,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Portland Halibut",
  "phone": null,
  "lat": 45.520988,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Portland Halibut",
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "1226 Oregon Coast Hwy",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.052868,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on Oregon Coast Hwy in Newport",
  "id": 4,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Halibut",
  "phone": null,
  "lat": 44.646006,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Newport Halibut",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
},
{
  "videos": [
    {
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "190 SW Maple St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.069126,
  "city": "Waldport",
  "zip": "97364",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on SW Maple St in Waldport",
  "id": 6,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Waldport Halibut",
  "phone": null,
  "lat": 44.425188,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Waldport Halibut",
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
},
{
  "videos": [
    {
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "facts": "",
  "street": "34455 Brooten Rd",
  "alt_name": "",
  "contact_name": "",
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "id": 8,
  "city": "Cloverdale",
  "zip": "97112",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "ext": {

  },
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Pacific City Halibut",
  "phone": null,
  "lat": 45.207253,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Pacific City Halibut",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "location_description": "Located on Brooten Rd in Pacific City",
  "lng": -123.959418,
  "history": ""
  }
  ]
}"""

        # Nearest 3 fish stores, with a proximity of 20 miles.
        self.expected_nearby_limit_3 = """
{
  "error": {
    "level": null,
    "status": false,
    "name": null,
    "debug": null,
    "text": null
  },
  "pointsofinterest": [{
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "1226 Oregon Coast Hwy",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.052868,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on Oregon Coast Hwy in Newport",
  "id": 4,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Halibut",
  "phone": null,
  "lat": 44.646006,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Newport Halibut",
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

        # When a bad limit is given, warn and ignore it.
        # This JSON contains the four stores in Newport and Waldport,
        # but not the Portland ones.
        self.expected_nearby_bad_limit = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad Limit",
    "debug": "ValueError: invalid literal for int() with base 10: 'cat'",
    "text": "Invalid limit. Returning all results."
  },
  "pointsofinterest": [{
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "1226 Oregon Coast Hwy",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.052868,
  "city": "Newport",
  "zip": "97365",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on Oregon Coast Hwy in Newport",
  "id": 4,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Newport Halibut",
  "phone": null,
  "lat": 44.646006,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Newport Halibut",
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
      "caption": "Princely",
      "link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
      "name": "Princely"
    }
  ],
  "images": [
    {
      "caption": "Woof!",
      "link": "/media/dog.jpg",
      "name": "A dog"
    }
  ],
  "street": "190 SW Maple St",
  "alt_name": "",
  "contact_name": "",
  "facts": "",
  "lng": -124.069126,
  "city": "Waldport",
  "zip": "97364",
  "hazards": [
    {
      "id": 2,
      "name": "Alien Abduction",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 4,
      "name": "Alien Abduction 4",
      "description": "This site is liable to result in you being abducted by aliens."
    },
    {
      "id": 6,
      "name": "Alien Abduction 6",
      "description": "This site is liable to result in you being abducted by aliens."
    }
  ],
  "location_description": "Located on SW Maple St in Waldport",
  "id": 6,
  "state": "OR",
  "email": "",
  "website": "",
  "description": "Fake Waldport Halibut",
  "phone": null,
  "lat": 44.425188,
  "categories": [
    {
      "category": "Uncool Stuff",
      "id": 2
    },
    {
      "category": "Non-Fish Shops",
      "id": 4
    },
    {
      "category": "Test Category Do Not Upvote",
      "id": 6
    }
  ],
  "name": "Waldport Halibut",
  "created": "2014-08-08T23:27:05.568Z",
  "modified": "2014-08-08T23:27:05.568Z",
  "ext": {

  },
  "history": ""
}]
}"""

    def test_successful_location_all_categories(self):
        """
        Test that good parameters return all pointsofinterest ordered by location.
        There will also be a default limit of 20 miles.
        """
        all_pointsofinterest_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538' % reverse('pois-list')
        ).content)

        expected_answer = json.loads(self.expected_nearby_all_pointsofinterest)

        for poi in all_pointsofinterest_data['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        self.assertEqual(all_pointsofinterest_data, expected_answer)

    def test_good_proximity_all_categories(self):
        """
        Test that good parameters return all pointsofinterest ordered by location.
        Extending the proximity to 50 miles adds two stores.
        """
        extended_proximity = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&'
            'proximity=50' % reverse('pois-list')).content)

        expected_answer = json.loads(self.expected_nearby_extended)
        self.assertEqual(extended_proximity, expected_answer)

    def test_bad_location_with_proximity_parameters(self):
        """
        Test that a bad location returns an error with good proximity.
        """
        all_pointsofinterest_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&lng=not_a_longitude&'
            'proximity=50' % reverse('pois-list')).content)

        expected_answer = json.loads(self.expected_error_result)

        all_pointsofinterest_data['pointsofinterest'] = sorted(
            all_pointsofinterest_data['pointsofinterest'], key=lambda k: k['id'])
        all_pointsofinterest_data['pointsofinterest'] = sorted(
            all_pointsofinterest_data['pointsofinterest'], key=lambda k: k['id'])
        expected_answer['pointsofinterest'] = sorted(
            expected_answer['pointsofinterest'], key=lambda k: k['id'])

        for poi in all_pointsofinterest_data['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        for poi in expected_answer['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])


        self.assertEqual(all_pointsofinterest_data, expected_answer)

    def test_bad_location_parameters(self):
        """
        Test that only one parameter (only lat/only long) returns a Warning,
        and that bad parameter values (text) return Warning.
        """

        # Coordinates are not numbers
        all_pointsofinterest_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&lng=not_a_longitude' % reverse(
                'pois-list')).content)

        expected_answer = json.loads(self.expected_error_result)

        all_pointsofinterest_data['pointsofinterest'] = sorted(
            all_pointsofinterest_data['pointsofinterest'], key=lambda k: k['id'])
        expected_answer['pointsofinterest'] = sorted(
            expected_answer['pointsofinterest'], key=lambda k: k['id'])

        for poi in all_pointsofinterest_data['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        for poi in expected_answer['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        self.assertEqual(all_pointsofinterest_data, expected_answer)

        # Lat is missing
        expected_answer = json.loads(self.expected_error_missing_lat)

        all_pointsofinterest_data = json.loads(self.client.get(
            '%s?lng=-45.232' % reverse('pois-list')).content)

        all_pointsofinterest_data['pointsofinterest'] = sorted(
            all_pointsofinterest_data['pointsofinterest'], key=lambda k: k['id'])
        expected_answer['pointsofinterest'] = sorted(
            expected_answer['pointsofinterest'], key=lambda k: k['id'])

        for poi in all_pointsofinterest_data['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        for poi in expected_answer['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        self.assertEqual(all_pointsofinterest_data, expected_answer)

        # Long is missing
        expected_answer = json.loads(self.expected_error_missing_long)

        all_pointsofinterest_data = json.loads(self.client.get(
            '%s?lat=-45.232' % reverse('pois-list')).content)
        all_pointsofinterest_data['pointsofinterest'] = sorted(
            all_pointsofinterest_data['pointsofinterest'], key=lambda k: k['id'])
        expected_answer['pointsofinterest'] = sorted(
            expected_answer['pointsofinterest'], key=lambda k: k['id'])

        for poi in all_pointsofinterest_data['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        for poi in expected_answer['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        self.assertEqual(all_pointsofinterest_data, expected_answer)

    def test_no_pointsofinterest_nearby(self):
        """
        Test that, when there are no pointsofinterest, we get an empty list back.
        """
        all_pointsofinterest_data = json.loads(self.client.get(
            '%s?lat=44.015225&lng=-123.016873' % reverse('pois-list')
        ).content)

        expected_answer = json.loads(self.expected_no_pointsofinterest)
        self.assertEqual(all_pointsofinterest_data, expected_answer)

    def test_limit_with_location_all_products(self):
        """
        Test that the limit parameter limits the number of pointsofinterest with the
        location parameters. There will also be a default proximity of
        20 miles.
        """
        all_pointsofinterest_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=3' % reverse(
                'pois-list')
            ).content)

        expected_answer = json.loads(self.expected_nearby_limit_3)

        for poi in all_pointsofinterest_data['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        for poi in expected_answer['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])


        self.assertEqual(all_pointsofinterest_data, expected_answer)

    def test_bad_limit_with_location_all_products(self):
        """
        Test that invalid limit parameters return an error.
        There will also be a default proximity of 20 miles.
        """
        all_pointsofinterest_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=cat' % reverse(
                'pois-list')).content)

        expected_answer = json.loads(self.expected_nearby_bad_limit)

        for poi in all_pointsofinterest_data['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        for poi in expected_answer['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        self.assertEqual(all_pointsofinterest_data, expected_answer)

    def test_limit_larger_than_length_all_products(self):
        """
        Test that a limit larger than the length of the list does not
        affect the list.
        """
        all_pointsofinterest_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&'
            'limit=200' % reverse('pois-list')).content)

        expected_answer = json.loads(self.expected_nearby_all_pointsofinterest)

        for poi in all_pointsofinterest_data['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        for poi in expected_answer['pointsofinterest']:
            poi['hazards'] = sorted(poi['hazards'], key=lambda k: k['id'])
            poi['categories'] = sorted(poi['categories'], key=lambda k: k['id'])

        self.assertEqual(all_pointsofinterest_data, expected_answer)
