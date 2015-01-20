from django.core.serializers import json
from working_waterfronts.working_waterfronts_api.models import (
    PointOfInterest, Hazard)


class FreshSerializer(json.Serializer):

    def get_dump_object(self, obj):
        self._current['id'] = obj.id

        if isinstance(obj, PointOfInterest):
            self._current['lat'] = obj.location.y
            self._current['lng'] = obj.location.x
            del self._current['location']

        if isinstance(obj, Hazard):
            del self._current['pointofinterests']

        self._current['ext'] = {}
        return self._current
