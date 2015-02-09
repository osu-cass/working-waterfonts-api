from django.shortcuts import render


def home(request):
    """
    */entry*

    Returns the /entry list, with buttons for Points of Interest, Hazards,
    and Categories.
    """
    return render(request, 'entry.html')
