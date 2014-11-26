from django.test import TestCase
from phonenumber_field.modelfields import PhoneNumberField

from whats_fresh.whats_fresh_api.models import POI
from django.contrib.gis.db import models


class POITestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'name': models.TextField,
            'description': models.TextField,
            'status': models.NullBooleanField,
            'street': models.TextField,
            'city': models.TextField,
            'state': models.TextField,
            'zip': models.TextField,
            'status': models.NullBooleanField,
            'location_description': models.TextField,
            'hours': models.TextField,
            'contact_name': models.TextField,
            'website': models.URLField,
            'email': models.EmailField,
            'phone': PhoneNumberField,
            'location': models.PointField,
            'story': models.ForeignKey,
            'story_id': models.ForeignKey,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'products_preparations': models.ManyToManyField,
            'poiproduct': models.related.RelatedObject,
            'id': models.AutoField
        }

        self.optional_fields = {
            'location_description',
            'website',
            'hours',
            'email',
            'phone'
        }

        self.null_fields = {'story', 'phone'}

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'POI')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = POI._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(POI._meta.get_field('modified').auto_now)
        self.assertTrue(POI._meta.get_field('created').auto_now_add)

    def test___unicode___method(self):
        try:
            POI.__unicode__(POI())
        except AttributeError:
            self.fail("No __unicode__ method found")

    def test_optional_fields(self):
        models.get_model('whats_fresh_api', 'POI')
        for field in self.optional_fields:
            self.assertEqual(
                POI._meta.get_field_by_name(field)[0].blank, True)
        for field in self.null_fields:
            self.assertEqual(
                POI._meta.get_field_by_name(field)[0].null, True)
