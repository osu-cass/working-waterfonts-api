from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import json


class POIsTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):

        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(
            reverse('login'), {'username': 'test', 'password': 'pass'})

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
  "pois": [
    {
      "id": 1,
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
      "story":  1,
      "ext": {

      },
      "created": "2014-08-08T23:27:05.568Z",
      "modified": "2014-08-08T23:27:05.568Z",
      "products": [
        {
          "product_id": 2,
          "name": "Starfish Voyager",
          "preparation": "Live",
          "preparation_id": 1
        },
        {
          "product_id": 1,
          "name": "Ezri Dax",
          "preparation": "Live",
          "preparation_id": 1
        }
      ]
    },
{
 "id": 2,
        "name": "All Optional Null Fields Are Null",
        "status": null,
        "description": "Ceci n'est pas un magasin.",
        "lat": 37.833688,
        "lng": -122.478002,
        "street": "501 Isabelle Rd",
        "city": "North Bend",
        "state": "OR",
        "zip": "97459",
        "location_description": "",
        "contact_name": "Isabelle",
        "phone": null,
        "hours": "",
        "website": "",
        "email": "",
        "story":  null,
        "ext": {},
        "created": "2014-08-08T23:27:05.568Z",
        "modified": "2014-08-08T23:27:05.568Z",
        "products": [
            {
                "product_id": 1,
                "name": "Ezri Dax",
                "preparation": "Live",
                "preparation_id": 1
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

    def test_limited_pois(self):
        response = self.client.get(
            "%s?limit=1" % reverse('pois-list')).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_limited_error)

        self.assertEqual(parsed_answer['error'], expected_answer['error'])
        self.assertEqual(len(parsed_answer['pois']), 1)


class NoPOIViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(
            reverse('login'), {'username': 'test', 'password': 'pass'})

        self.expected_no_pois = """
{
  "error": {
    "status": true,
    "text": "No POIs found",
    "name": "No POIs",
    "debug": "",
    "level": "Information"
  },
  "pois": []
}"""

    def test_no_products(self):
        response = self.client.get(reverse('pois-list'))

        parsed_answer = json.loads(response.content)
        expected_answer = json.loads(self.expected_no_pois)
        self.assertEqual(response.status_code, 200)

        expected_answer = json.loads(self.expected_no_pois)

        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)


class POIsLocationTestCase(TestCase):

    """
    Test whether the /pois/ view returns the correct results when given a
    coordinate to center on.

    For future test-writers: the location_fixtures tests have six pois
    in them -- two in Newport, two in Waldport, and two in Portland. Each
    poi has one product, and each product is sold at one of the two pois
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
        self.client.post(
            reverse('login'), {'username': 'test', 'password': 'pass'})

        self.maxDiff = None

        # No pois. This is the return for location queries from
        # the middle of nowhere.
        self.expected_no_pois = """
{
  "error": {
            "debug": "",
            "status": true,
            "level": "Information",
            "text": "No POIs found",
            "name": "No POIs"
  },
  "pois": []
}"""

        # All fish around Newport
        # This JSON contains the four stores in Newport and Waldport,
        # but not the Portland ones.
        self.expected_nearby_all_pois = """
{
  "error": {
    "level": null,
    "status": false,
    "name": null,
    "debug": null,
    "text": null
  },
  "pois": [{
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "lng": -124.050122,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "lng": -124.052868,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "lng": -124.066166,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 6,
    "website": "",
    "street": "190 SW Maple St",
    "contact_name": "Waldport Halibut Contact",
    "city": "Waldport",
    "story":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "lng": -124.069126,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  }]
}"""

        # All fish around Newport, with extended proximity.
        # This JSON contains the six stores in Newport, Waldport, Pacific City
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
  "pois": [
    {
      "status": true,
      "city": "Newport",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Newport Tuna",
      "zip": "97365",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 2,
      "ext": {

      },
      "location_description": "Located on Bay Blvd in Newport",
      "lng": -124.050122,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "146 SE Bay Blvd",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 2,
          "name": "Tuna"
        }
      ],
      "lat": 44.631592,
      "contact_name": "Newport Tuna Contact",
      "id": 3,
      "name": "Newport Tuna"
    },
    {
      "status": true,
      "city": "Newport",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Newport Halibut",
      "zip": "97365",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 1,
      "ext": {

      },
      "location_description": "Located on Oregon Coast Hwy in Newport",
      "lng": -124.052868,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "1226 Oregon Coast Hwy",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 1,
          "name": "Halibut"
        }
      ],
      "lat": 44.646006,
      "contact_name": "Newpotr Halibut Contact",
      "id": 4,
      "name": "Newport Halibut"
    },
    {
      "status": true,
      "city": "Waldport",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Waldport Tuna",
      "zip": "97394",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 2,
      "ext": {

      },
      "location_description": "Located on Spring St in Waldport",
      "lng": -124.066166,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "522 NW Spring St",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 2,
          "name": "Tuna"
        }
      ],
      "lat": 44.427761,
      "contact_name": "Waldport Tuna Contact",
      "id": 5,
      "name": "Waldport Tuna"
    },
    {
      "status": true,
      "city": "Waldport",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Waldport Halibut",
      "zip": "97364",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 1,
      "ext": {

      },
      "location_description": "Located on SW Maple St in Waldport",
      "lng": -124.069126,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "190 SW Maple St",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 1,
          "name": "Halibut"
        }
      ],
      "lat": 44.425188,
      "contact_name": "Waldport Halibut Contact",
      "id": 6,
      "name": "Waldport Halibut"
    },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 2,
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "lng": -123.958093,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 2,
          "name": "Tuna"
        }
      ],
      "lat": 45.197105,
      "contact_name": "Pacific City Tuna Contact",
      "id": 7,
      "name": "Pacific City Tuna"
    },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Halibut",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 1,
      "ext": {

      },
      "location_description": "Located on Brooten Rd in Pacific City",
      "lng": -123.959418,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "34455 Brooten Rd",
      "products": [
        {
          "preparation": "Frozen",
          "preparation_id": 1,
          "product_id": 1,
          "name": "Halibut"
        }
      ],
      "lat": 45.207253,
      "contact_name": "Pacific City Halibut Contact",
      "id": 8,
      "name": "Pacific City Halibut"
    }
  ]
}"""

        # All pois for all products
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
  "pois": [
  {
    "id": 1,
    "website": "",
    "street": "720 SW Broadway",
    "contact_name": "Portland Tuna Contact",
    "city": "Portland",
    "story":  2,
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "lng": -122.67963,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Tuna",
    "phone": null,
    "lat": 45.518962,
    "name": "Portland Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "lng": -124.050122,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 2,
    "website": "",
    "street": "1 SW Pine St",
    "contact_name": "Portland Halibut Contact",
    "city": "Portland",
    "story":  1,
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "lng": -122.670619,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Halibut",
    "phone": null,
    "lat": 45.520988,
    "name": "Portland Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "lng": -124.066166,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "lng": -124.052868,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 6,
    "website": "",
    "street": "190 SW Maple St",
    "contact_name": "Waldport Halibut Contact",
    "city": "Waldport",
    "story":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "lng": -124.069126,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
       {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 2,
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "lng": -123.958093,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
      ],
      "lat": 45.197105,
      "contact_name": "Pacific City Tuna Contact",
      "id": 7,
      "name": "Pacific City Tuna"
    },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Halibut",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 1,
      "ext": {

      },
      "location_description": "Located on Brooten Rd in Pacific City",
      "lng": -123.959418,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "34455 Brooten Rd",
      "products": [
       {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
      ],
      "lat": 45.207253,
      "contact_name": "Pacific City Halibut Contact",
      "id": 8,
      "name": "Pacific City Halibut"
    }
  ]
}"""

        # All pois for all products
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
  "pois": [
  {
    "id": 1,
    "website": "",
    "street": "720 SW Broadway",
    "contact_name": "Portland Tuna Contact",
    "city": "Portland",
    "story":  2,
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "lng": -122.67963,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Tuna",
    "phone": null,
    "lat": 45.518962,
    "name": "Portland Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "lng": -124.050122,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 2,
    "website": "",
    "street": "1 SW Pine St",
    "contact_name": "Portland Halibut Contact",
    "city": "Portland",
    "story":  1,
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "lng": -122.670619,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Halibut",
    "phone": null,
    "lat": 45.520988,
    "name": "Portland Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "lng": -124.066166,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "lng": -124.052868,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 6,
    "website": "",
    "street": "190 SW Maple St",
    "contact_name": "Waldport Halibut Contact",
    "city": "Waldport",
    "story":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "lng": -124.069126,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
       {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 2,
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "lng": -123.958093,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
      ],
      "lat": 45.197105,
      "contact_name": "Pacific City Tuna Contact",
      "id": 7,
      "name": "Pacific City Tuna"
    },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Halibut",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 1,
      "ext": {

      },
      "location_description": "Located on Brooten Rd in Pacific City",
      "lng": -123.959418,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "34455 Brooten Rd",
      "products": [
       {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
      ],
      "lat": 45.207253,
      "contact_name": "Pacific City Halibut Contact",
      "id": 8,
      "name": "Pacific City Halibut"
    }
  ]
}"""

        # All pois for all products
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
  "pois": [
  {
    "id": 1,
    "website": "",
    "street": "720 SW Broadway",
    "contact_name": "Portland Tuna Contact",
    "city": "Portland",
    "story":  2,
    "zip": "97204",
    "location_description": "Located on Broadway in Portland",
    "lng": -122.67963,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Tuna",
    "phone": null,
    "lat": 45.518962,
    "name": "Portland Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "lng": -124.050122,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 2,
    "website": "",
    "street": "1 SW Pine St",
    "contact_name": "Portland Halibut Contact",
    "city": "Portland",
    "story":  1,
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "lng": -122.670619,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Portland Halibut",
    "phone": null,
    "lat": 45.520988,
    "name": "Portland Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "lng": -124.066166,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "lng": -124.052868,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 6,
    "website": "",
    "street": "190 SW Maple St",
    "contact_name": "Waldport Halibut Contact",
    "city": "Waldport",
    "story":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "lng": -124.069126,
    "state": "OR",
    "hours": "",
    "email": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
       {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Tuna",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 2,
      "ext": {

      },
      "location_description": "Located on Roger Ave in Pacific City",
      "lng": -123.958093,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "35650 Roger Ave",
      "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
      ],
      "lat": 45.197105,
      "contact_name": "Pacific City Tuna Contact",
      "id": 7,
      "name": "Pacific City Tuna"
    },
    {
      "status": true,
      "city": "Cloverdale",
      "website": "",
      "modified": "2014-08-08T23:27:05.568Z",
      "description": "Fake Pacific City Halibut",
      "zip": "97112",
      "created": "2014-08-08T23:27:05.568Z",
      "story": 1,
      "ext": {

      },
      "location_description": "Located on Brooten Rd in Pacific City",
      "lng": -123.959418,
      "email": "",
      "hours": "",
      "phone": null,
      "state": "OR",
      "street": "34455 Brooten Rd",
      "products": [
       {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
      ],
      "lat": 45.207253,
      "contact_name": "Pacific City Halibut Contact",
      "id": 8,
      "name": "Pacific City Halibut"
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
  "pois": [{
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "lng": -124.050122,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "lng": -124.052868,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "lng": -124.066166,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
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
  "pois": [{
    "id": 3,
    "website": "",
    "street": "146 SE Bay Blvd",
    "contact_name": "Newport Tuna Contact",
    "city": "Newport",
    "story":  2,
    "zip": "97365",
    "location_description": "Located on Bay Blvd in Newport",
    "lng": -124.050122,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Tuna",
    "phone": null,
    "lat": 44.631592,
    "name": "Newport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 4,
    "website": "",
    "street": "1226 Oregon Coast Hwy",
    "contact_name": "Newpotr Halibut Contact",
    "city": "Newport",
    "story":  1,
    "zip": "97365",
    "location_description": "Located on Oregon Coast Hwy in Newport",
    "lng": -124.052868,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Newport Halibut",
    "phone": null,
    "lat": 44.646006,
    "name": "Newport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
  },
  {
    "id": 5,
    "website": "",
    "street": "522 NW Spring St",
    "contact_name": "Waldport Tuna Contact",
    "city": "Waldport",
    "story":  2,
    "zip": "97394",
    "location_description": "Located on Spring St in Waldport",
    "lng": -124.066166,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Tuna",
    "phone": null,
    "lat": 44.427761,
    "name": "Waldport Tuna",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 2,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Tuna"
      }
    ]
  },
  {
    "id": 6,
    "website": "",
    "street": "190 SW Maple St",
    "contact_name": "Waldport Halibut Contact",
    "city": "Waldport",
    "story":  1,
    "zip": "97364",
    "location_description": "Located on SW Maple St in Waldport",
    "lng": -124.069126,
    "state": "OR",
    "email": "",
    "hours": "",
    "status": true,
    "modified": "2014-08-08T23:27:05.568Z",
    "description": "Fake Waldport Halibut",
    "phone": null,
    "lat": 44.425188,
    "name": "Waldport Halibut",
    "created": "2014-08-08T23:27:05.568Z",
    "ext": {

    },
    "products": [
      {
        "product_id": 1,
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  }]
}"""

    def test_successful_location_all_products(self):
        """
        Test that good parameters return all pois ordered by location.
        There will also be a default limit of 20 miles.
        """
        all_pois_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538' % reverse('pois-list')
        ).content)

        expected_answer = json.loads(self.expected_nearby_all_pois)
        self.assertEqual(all_pois_data, expected_answer)

    def test_good_proximity_all_products(self):
        """
        Test that good parameters return all pois ordered by location.
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
        all_pois_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&lng=not_a_longitude&'
            'proximity=50' % reverse('pois-list')).content)

        expected_answer = json.loads(self.expected_error_result)

        all_pois_data['pois'] = sorted(
            all_pois_data['pois'], key=lambda k: k['id'])
        expected_answer['pois'] = sorted(
            expected_answer['pois'], key=lambda k: k['id'])

        self.assertEqual(all_pois_data, expected_answer)

    def test_bad_location_parameters(self):
        """
        Test that only one parameter (only lat/only long) returns a Warning,
        and that bad parameter values (text) return Warning.
        """

        # Coordinates are not numbers
        all_pois_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&lng=not_a_longitude' % reverse(
                'pois-list')).content)

        expected_answer = json.loads(self.expected_error_result)

        all_pois_data['pois'] = sorted(
            all_pois_data['pois'], key=lambda k: k['id'])
        expected_answer['pois'] = sorted(
            expected_answer['pois'], key=lambda k: k['id'])

        for poi in all_pois_data['pois']:
            for product in poi['products']:
                self.assertTrue('product_id' in product)

        for poi in expected_answer['pois']:
            poi['products'] = sorted(
                poi['products'], key=lambda k: k['product_id'])

        for poi in all_pois_data['pois']:
            poi['products'] = sorted(
                poi['products'], key=lambda k: k['product_id'])

        self.assertEqual(all_pois_data, expected_answer)

        # Lat is missing
        expected_answer = json.loads(self.expected_error_missing_lat)

        all_pois_data = json.loads(self.client.get(
            '%s?lng=-45.232' % reverse('pois-list')).content)

        all_pois_data['pois'] = sorted(
            all_pois_data['pois'], key=lambda k: k['id'])
        expected_answer['pois'] = sorted(
            expected_answer['pois'], key=lambda k: k['id'])

        for poi in all_pois_data['pois']:
            for product in poi['products']:
                self.assertTrue('product_id' in product)

        for poi in expected_answer['pois']:
            poi['products'] = sorted(
                poi['products'], key=lambda k: k['product_id'])

        for poi in all_pois_data['pois']:
            poi['products'] = sorted(
                poi['products'], key=lambda k: k['product_id'])

        self.assertEqual(all_pois_data, expected_answer)

        # Long is missing
        expected_answer = json.loads(self.expected_error_missing_long)

        all_pois_data = json.loads(self.client.get(
            '%s?lat=-45.232' % reverse('pois-list')).content)
        all_pois_data['pois'] = sorted(
            all_pois_data['pois'], key=lambda k: k['id'])
        expected_answer['pois'] = sorted(
            expected_answer['pois'], key=lambda k: k['id'])

        for poi in expected_answer['pois']:
            poi['products'] = sorted(
                poi['products'], key=lambda k: k['product_id'])

        for poi in all_pois_data['pois']:
            poi['products'] = sorted(
                poi['products'], key=lambda k: k['product_id'])

        self.assertEqual(all_pois_data, expected_answer)

    def test_no_pois_nearby(self):
        """
        Test that, when there are no pois, we get an empty list back.
        """
        all_pois_data = json.loads(self.client.get(
            '%s?lat=44.015225&lng=-123.016873' % reverse('pois-list')
        ).content)

        expected_answer = json.loads(self.expected_no_pois)
        self.assertEqual(all_pois_data, expected_answer)

    def test_limit_with_location_all_products(self):
        """
        Test that the limit parameter limits the number of pois with the
        location parameters. There will also be a default proximity of
        20 miles.
        """
        all_pois_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=3' % reverse(
                'pois-list')
            ).content)

        expected_answer = json.loads(self.expected_nearby_limit_3)
        self.assertEqual(all_pois_data, expected_answer)

    def test_bad_limit_with_location_all_products(self):
        """
        Test that invalid limit parameters return an error.
        There will also be a default proximity of 20 miles.
        """
        all_pois_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=cat' % reverse(
                'pois-list')).content)

        expected_answer = json.loads(self.expected_nearby_bad_limit)
        self.assertEqual(all_pois_data, expected_answer)

    def test_limit_larger_than_length_all_products(self):
        """
        Test that a limit larger than the length of the list does not
        affect the list.
        """
        all_pois_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&'
            'limit=200' % reverse('pois-list')).content)

        expected_answer = json.loads(self.expected_nearby_all_pois)
        self.assertEqual(all_pois_data, expected_answer)
