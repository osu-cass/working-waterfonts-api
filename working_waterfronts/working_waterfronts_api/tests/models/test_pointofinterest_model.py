from django.test import TestCase
from phonenumber_field.modelfields import PhoneNumberField

from working_waterfronts.working_waterfronts_api.models import PointOfInterest
from django.contrib.gis.db import models


class PointOfInterestTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'name': models.TextField,
            'alt_name': models.TextField,
            'contact_name': models.TextField,
            'location': models.PointField,
            'street': models.TextField,
            'city': models.TextField,
            'state': models.TextField,
            'zip': models.TextField,
            'description': models.TextField,
            'history': models.TextField,
            'facts': models.TextField,
            'location_description': models.TextField,
            'website': models.URLField,
            'email': models.EmailField,
            'phone': PhoneNumberField,
            'hazards': models.ManyToManyField,
            'categories': models.ManyToManyField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            u'id': models.AutoField
        }

        self.optional_fields = {
            'alt_name',
            'location_description',
            'website',
            'email',
            'phone'
        }

        self.null_fields = {'phone'}

    def test_fields_exist(self):
        model = PointOfInterest
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = PointOfInterest._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(PointOfInterest._meta.get_field('modified').auto_now)
        self.assertTrue(PointOfInterest._meta.get_field('created').auto_now_add)

    def test___unicode___method(self):
        assert hasattr(PointOfInterest, '__unicode__'), "No __unicode__ method found"

    def test_optional_fields(self):
        for field in self.optional_fields:
            self.assertEqual(
                PointOfInterest._meta.get_field_by_name(field)[0].blank, True)
        for field in self.null_fields:
            self.assertEqual(
                PointOfInterest._meta.get_field_by_name(field)[0].null, True)
