from django.test import TestCase

from whats_fresh.whats_fresh_api.models import Preparation
from django.contrib.gis.db import models


class PreparationsTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'name': models.TextField,
            'description': models.TextField,
            'additional_info': models.TextField,
            'productpreparation': models.related.RelatedObject,
            'products': models.related.RelatedObject,
            'id': models.AutoField
        }

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'Preparation')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Preparation._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def test___unicode___method(self):
        try:
            Preparation.__unicode__(Preparation())
        except AttributeError:
            self.fail("No __unicode__ method found")
