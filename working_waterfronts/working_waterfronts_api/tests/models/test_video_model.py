from django.test import TestCase

from working_waterfronts.working_waterfronts_api.models import Video
from django.contrib.gis.db import models


class VideoTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'video': models.URLField,
            'caption': models.TextField,
            'name': models.TextField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'pointofinterest': models.related.RelatedObject,
            'id': models.AutoField
        }

        self.optional_fields = {
            'caption'
        }

    def test_fields_exist(self):
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(Video._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Video._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(Video._meta.get_field('modified').auto_now)
        self.assertTrue(Video._meta.get_field('created').auto_now_add)

    def test_optional_fields(self):
        for field in self.optional_fields:
            self.assertEqual(
                Video._meta.get_field_by_name(field)[0].blank, True)

    def test___unicode___method(self):
        assert hasattr(Video, '__unicode__'), "No __unicode__ method found"
