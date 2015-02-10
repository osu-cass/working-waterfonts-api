from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """
    */entry*

    Returns the /entry list, with buttons for Points of Interest, Hazards,
    and Categories.
    """
    return render(request, 'entry.html')
