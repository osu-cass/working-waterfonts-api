from django.test import TestCase

from working_waterfronts.working_waterfronts_api.models import (POIProduct,
                                                ProductPreparation, Product,
                                                Preparation, POI)
from django.contrib.gis.db import models


class POIProductJoinTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'poi': models.ForeignKey,
            'poi_id': models.ForeignKey,
            'product_preparation': models.ForeignKey,
            'product_preparation_id': models.ForeignKey,
            'poi_price': models.TextField,
            'available': models.NullBooleanField,
            'id': models.AutoField
        }

        self.optional_fields = {
            'poi_price',
            'available'
        }

    def test_fields_exist(self):
        model = models.get_model('working_waterfronts_api', 'POIProduct')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = POIProduct._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test___unicode___method(self):
        try:
            POIProduct.__unicode__(
                POIProduct(
                    poi=POI(name='test'),
                    product_preparation=ProductPreparation(
                        product=Product(name='test'),
                        preparation=Preparation(name='test')
                    )
                ))
        except AttributeError:
            self.fail("No __unicode__ method found")

    def test_optional_fields(self):
        models.get_model('working_waterfronts_api', 'POIProduct')
        for field in self.optional_fields:
            self.assertEqual(
                POIProduct._meta.get_field_by_name(field)[0].blank, True)
