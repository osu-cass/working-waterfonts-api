from django.test import TestCase

from working_waterfronts.working_waterfronts_api.models import (PointOfInterest,
                                                                Hazard)
from django.contrib.gis.db import models


class PointOfInteresthazardTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'pointofinterest': models.ForeignKey,
            'pointofinterest_id': models.ForeignKey,
            'hazard': models.ForeignKey,
            'hazard_id': models.ForeignKey,
            'id': models.AutoField
        }

    def test_fields_exist(self):
        model = models.get_model('working_waterfronts_api',
                'PointOfInterestHazard')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = PointOfInterestHazard._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test___unicode___method(self):
        try:
            PointOfInterestHazard.__unicode__(
                PointOfInterestHazard(
                    pointofinterest=PointOfInterest(name='test'),
                    hazard=Hazard(name='test')
                ))
        except AttributeError:
            self.fail("No __unicode__ method found")
