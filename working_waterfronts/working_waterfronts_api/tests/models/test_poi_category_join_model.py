from django.test import TestCase

from working_waterfronts.working_waterfronts_api.models import (POICateogry)
from django.contrib.gis.db import models


class POICategoryJoinTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'poi': models.ForeignKey,
            'poi_id': models.ForeignKey,
            'category': models.TextField,
            'id': models.AutoField
        }

        self.optional_fields = {}

    def test_fields_exist(self):
        model = models.get_model('working_waterfronts_api', 'POICateogry')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = POICategory._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test___unicode___method(self):
        try:
            POICategory.__unicode__(
                POICategory(
                    poi=POI(name='test'),
                    category=Category(category='test')))
        except AttributeError:
            self.fail("No __unicode__ method found")

    def test_optional_fields(self):
        models.get_model('working_waterfronts_api', 'POICategory')
        for field in self.optional_fields:
            self.assertEqual(
                POICategory._meta.get_field_by_name(field)[0].blank, True)
