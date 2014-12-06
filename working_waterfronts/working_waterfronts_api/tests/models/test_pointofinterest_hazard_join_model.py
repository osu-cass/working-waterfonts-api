from django.test import TestCase

from working_waterfronts.working_waterfronts_api.models import (PointOfInterestCateogry)
from django.contrib.gis.db import models


class PointOfInterestCategoryJoinTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'pointofinterest': models.ForeignKey,
            'pointofinterest_id': models.ForeignKey,
            'hazard': models.ForeignKey,
            'hazard_id': models.ForeignKey,
            'id': models.AutoField
        }

    def test_fields_exist(self):
        model = models.get_model('working_waterfronts_api', 'PointOfInterestCateogry')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = PointOfInterestCategory._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test___unicode___method(self):
        assert hasattr(PointOfInterestCategory, '__unicode__'), "No __unicode__ method found"
