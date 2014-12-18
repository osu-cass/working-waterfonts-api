from django.test import TestCase

from working_waterfronts.working_waterfronts_api.models import Category
from django.contrib.gis.db import models


class CategoryTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'category': models.TextField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'pointofinterestcategory': models.related.RelatedObject,
            'id': models.AutoField
        }

    def test_fields_exist(self):
        model = Category
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Category._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(Category._meta.get_field('modified').auto_now)
        self.assertTrue(Category._meta.get_field('created').auto_now_add)

    def test___unicode___method(self):
        assert hasattr(Category, '__unicode__'), "No __unicode__ method found"