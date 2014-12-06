from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from working_waterfronts.working_waterfronts_api.functions import group_required


@login_required
@group_required('Administration Users', 'Data Entry Users')
def home(request):
    """
    */entry*

    Returns the /entry list, with buttons for PointOfInterests, Products,
    and Preparations.
    """
    return render(request, 'entry.html')
