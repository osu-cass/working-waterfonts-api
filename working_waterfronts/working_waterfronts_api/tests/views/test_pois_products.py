from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import json


class POIsProductsTestCase(TestCase):
    fixtures = ['overlapping_fixtures']

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(reverse('login'), {'username': 'test',
                                            'password': 'pass'})

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
  "pois": [
    {
      "id": 10,
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
      "story":  10,
      "ext": {

      },
      "created": "2014-08-08T23:27:05.568Z",
      "modified": "2014-08-08T23:27:05.568Z",
      "products": [
        {
          "product_id": 10,
          "name": "Starfish Voyager",
          "preparation": "Live",
          "preparation_id": 10
        },
        {
          "product_id": 100,
          "name": "Ezri Dax",
          "preparation": "Live",
          "preparation_id": 10
        }
      ]
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
        url = reverse('pois-products', kwargs={'id': '10'})
        self.assertEqual(url, '/1/pois/products/10')

    def test_no_location_parameter(self):
        response = self.client.get(
            reverse('pois-products', kwargs={'id': '10'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)

        parsed_answer['pois'] = sorted(
            parsed_answer['pois'], key=lambda k: k['id'])
        expected_answer['pois'] = sorted(
            expected_answer['pois'], key=lambda k: k['id'])

        for poi in parsed_answer['pois']:
            for product in poi['products']:
                self.assertTrue('product_id' in product)

        for poi in expected_answer['pois']:
            poi['products'] = sorted(
                poi['products'], key=lambda k: k['product_id'])

        for poi in parsed_answer['pois']:
            poi['products'] = sorted(
                poi['products'], key=lambda k: k['product_id'])

        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)

    def test_limit_parameter(self):
        response = self.client.get(
            "%s?limit=1" % reverse(
                'pois-products', kwargs={'id': '100'})
        ).content

        parsed_answer = json.loads(response)
        expected_error = json.loads(self.limited_pois_error)

        self.assertEqual(parsed_answer['error'], expected_error['error'])
        self.assertEqual(len(parsed_answer['pois']), 1)


class POIsProductsLocationTestCase(TestCase):

    """
    Test whether the /pois/products/<id> view returns the correct results
    when given a coordinate to center on.

    This is an individual class to allow the use of different fixture sets.

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
    "text": "No POIs found for product 1",
    "name": "No POIs"
    },
  "pois": []
}"""

        # Nearby pois for product Halibut (1)
        # This JSON contains the two halibut stores in Newport and Waldport,
        # but not Portland. This is the return for a good coordinates.
        self.expected_halibut = """
{
  "error": {
    "level": null,
    "status": false,
    "name": null,
    "debug": null,
    "text": null
  },
  "pois": [{
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

        # Nearby pois for product Halibut (1), with 50 mile range.
        # This JSON contains the halibut stores in Newport, Waldport, and
        # Pacific City, but not Portland. This is the return for a good
        # coordinates.
        self.expected_halibut_extended = """
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

        # Nearby pois for product Halibut (1)
        # This JSON contains the two halibut stores in Newport and Waldport,
        # but not Portland. This is the return for a good coordinates.
        self.expected_halibut_bad_limit = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "name": "Bad Limit",
    "debug": "ValueError: invalid literal for int() with base 10: 'cat'",
    "text": "Invalid limit. Returning all results."
  },
  "pois": [{
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

        # Nearby pois for product Halibut (1)
        # This JSON contains the two halibut stores in Newport and Waldport,
        # but not Portland. This is the return for a good coordinates.
        self.expected_halibut_limit_1 = """
{
  "error": {
    "level": null,
    "status": false,
    "name": null,
    "debug": null,
    "text": null
  },
  "pois": [{
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
        "preparation_id": 1,
        "preparation": "Frozen",
        "name": "Halibut"
      }
    ]
  }]
}"""

        # All pois for product Halibut (1)
        # This JSON contains the three halibut stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
        self.expected_all_pois_products = """
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
  "pois": [{
    "id": 2,
    "name": "Portland Halibut",
    "status": true,
    "description": "Fake Portland Halibut",
    "lat": 45.520988,
    "lng": -122.670619,
    "street": "1 SW Pine St",
    "city": "Portland",
    "state": "OR",
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "contact_name": "Portland Halibut Contact",
    "phone": null,
    "story":  1,
    "hours": "",
    "website": "",
    "email": "",
    "created": "2014-08-08T23:27:05.568Z",
    "modified": "2014-08-08T23:27:05.568Z",
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
  },{
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
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
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
    }]
}"""

        # All pois for product Halibut (1)
        # This JSON contains the three halibut stores in Newport, Waldport,
        # and Portland. This is the return for a bad proximity with good
        # location -- the default proximity of 20 miles.
        self.expected_vp_bad_prox = """
{
  "error": {
    "level": "Warning",
    "status": true,
    "text": "There was an error finding pois within cat miles",
    "name": "Bad proximity",
    "debug": "ValueError: invalid literal for int() with base 10: 'cat'"
  },
  "pois": [{
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

        # All pois for product Halibut (1)
        # This JSON contains the three halibut stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
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
  "pois": [{
    "id": 2,
    "name": "Portland Halibut",
    "status": true,
    "description": "Fake Portland Halibut",
    "lat": 45.520988,
    "lng": -122.670619,
    "street": "1 SW Pine St",
    "city": "Portland",
    "state": "OR",
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "contact_name": "Portland Halibut Contact",
    "phone": null,
    "story":  1,
    "hours": "",
    "website": "",
    "email": "",
    "created": "2014-08-08T23:27:05.568Z",
    "modified": "2014-08-08T23:27:05.568Z",
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
  },{
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
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
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
    }]
}"""

        # All pois for product Halibut (1)
        # This JSON contains the three halibut stores in Newport, Waldport,
        # and Portland. This is the return for a bad coordinates.
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
  "pois": [{
    "id": 2,
    "name": "Portland Halibut",
    "status": true,
    "description": "Fake Portland Halibut",
    "lat": 45.520988,
    "lng": -122.670619,
    "street": "1 SW Pine St",
    "city": "Portland",
    "state": "OR",
    "zip": "97204",
    "location_description": "Located on Pine in Portland",
    "contact_name": "Portland Halibut Contact",
    "phone": null,
    "story":  1,
    "hours": "",
    "website": "",
    "email": "",
    "created": "2014-08-08T23:27:05.568Z",
    "modified": "2014-08-08T23:27:05.568Z",
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
  },{
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
        "preparation": "Frozen",
        "preparation_id": 1,
        "name": "Halibut"
      }
    ]
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
    }]
}"""

    def test_no_pois_nearby_poi_products(self):
        """
        Test that, when there are no pois, we get an empty list back for the
        pois/products endpoint.
        """
        no_poi_data = json.loads(
            self.client.get(
                '%s?lat=44.015225&lng=-123.016873' % reverse(
                    'pois-products', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_no_pois)
        self.assertEqual(no_poi_data, expected_answer)

    def test_successful_location_by_poi_product(self):
        """
        Test that good parameters return poi/product results ordered by
        location. There will also be a default limit of 20 miles.
        """
        halibut_near_newport = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538' % reverse('pois-products',
                                                         kwargs={'id': '1'})
        ).content)

        expected_answer = json.loads(self.expected_halibut)
        self.assertEqual(halibut_near_newport, expected_answer)

    def test_good_limit_by_poi_product(self):
        """
        Test that good parameters return poi/product results ordered by
        location. There will also be a default limit of 20 miles.
        """
        halibut_near_newport_limit = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=1' % reverse(
                'pois-products', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_halibut_limit_1)
        self.assertEqual(halibut_near_newport_limit, expected_answer)

    def test_limit_larger_than_length_all_products(self):
        """
        Test that a limit larger than the length of the list does not
        affect the list.
        """
        halibut_near_newport = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=10' % reverse(
                'pois-products', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_halibut)
        self.assertEqual(halibut_near_newport, expected_answer)

    def test_bad_limit_by_poi_product(self):
        """
        Test that good parameters return poi/product results ordered by
        location. There will also be a default limit of 20 miles.
        """
        halibut_near_newport_limit = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&limit=cat' % reverse(
                'pois-products', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_halibut_bad_limit)
        self.assertEqual(halibut_near_newport_limit, expected_answer)

    def test_bad_location_parameters_poi_products(self):
        """
        Test that only one parameter (only lat/only long) returns a Warning,
        and that bad parameter values (text) return Warning, for the
        pois/products endpoint.
        """

        # Coordinates are not numbers
        broken_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&lng=not_a_longitude' % reverse(
                'pois-products', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_all_pois_products)
        self.assertEqual(broken_data, expected_answer)

        # lat is missing
        broken_data = json.loads(self.client.get(
            '%s?lng=-45.232' % reverse(
                'pois-products', kwargs={'id': '1'})).content)
        expected_answer = json.loads(self.expected_all_missing_lat)

        self.assertEqual(broken_data, expected_answer)

        # long is missing
        broken_data = json.loads(self.client.get(
            '%s?lat=-45.232' % reverse(
                'pois-products', kwargs={'id': '1'})).content)
        expected_answer = json.loads(self.expected_all_missing_long)

        self.assertEqual(broken_data, expected_answer)

    def test_successful_location_by_poi_product_extended_proximity(self):
        """
        Test that good parameters return poi/product results ordered by
        location, with an extended proximity of 50 miles. This will include
        the Pacific City location.
        """
        halibut_near_newport_extended = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538'
            '&proximity=50' % reverse(
                'pois-products', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_halibut_extended)
        self.assertEqual(halibut_near_newport_extended, expected_answer)

    def test_proximity_bad_location_poi_products(self):
        """
        Test that bad location returns a Warning.
        """
        # Good proximity, bad location
        broken_data = json.loads(self.client.get(
            '%s?lat=not_a_latitude&lng=not_a_longitude&proximity=50' % reverse(
                'pois-products', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_all_pois_products)
        self.assertEqual(broken_data, expected_answer)

    def test_bad_proximity_good_location_poi_products(self):
        """
        Test that bad proximity returns a Warning.
        """
        broken_data = json.loads(self.client.get(
            '%s?lat=44.609079&lng=-124.052538&proximity=cat' % reverse(
                'pois-products', kwargs={'id': '1'})).content)

        expected_answer = json.loads(self.expected_vp_bad_prox)
        self.assertEqual(broken_data, expected_answer)
