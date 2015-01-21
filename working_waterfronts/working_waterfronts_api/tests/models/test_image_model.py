from django.test import TestCase

from working_waterfronts.working_waterfronts_api.models import Image
from django.contrib.gis.db import models


class ImageTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'image': models.ImageField,
            'name': models.TextField,
            'caption': models.TextField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'pointofinterest': models.related.RelatedObject,
            'id': models.AutoField
        }

        self.optional_fields = {
            'caption'
        }

    def test_fields_exist(self):
        model = Image
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_parameters(self):
        self.assertEqual(
            Image._meta.get_field_by_name('image')[0].upload_to,
            'images')

    def test_no_additional_fields(self):
        fields = Image._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(Image._meta.get_field('modified').auto_now)
        self.assertTrue(Image._meta.get_field('created').auto_now_add)

    def test_filename_method(self):
        assert hasattr(Image, 'filename'), "No filename() method found"

    def test___unicode___method(self):
        assert hasattr(Image, '__unicode__'), "No __unicode__ method found"

    def test_optional_fields(self):
        for field in self.optional_fields:
            self.assertEqual(
                Image._meta.get_field_by_name(field)[0].blank, True)
