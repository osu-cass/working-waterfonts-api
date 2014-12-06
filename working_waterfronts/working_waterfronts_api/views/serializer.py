from django.core.serializers import json
from working_waterfronts.working_waterfronts_api.models import PointOfInterest


class FreshSerializer(json.Serializer):

    def get_dump_object(self, obj):
        self._current['id'] = obj.id

        if isinstance(obj, PointOfInterest):
            self._current['lat'] = obj.location.y
            self._current['lng'] = obj.location.x
            del self._current['location']

            self._current['products'] = [
                {
                    'name': pp.product.name,
                    'preparation': pp.preparation.name,
                    'product_id': pp.product.id,
                    'preparation_id': pp.preparation_id
                }
                for pp in obj.products_preparations.all()
            ]

        self._current['ext'] = {}
        return self._current
