import django.forms as forms
from working_waterfronts.working_waterfronts_api.models import (
    Hazard, Image, Video, PointOfInterest, Category)


class PointOfInterestForm(forms.ModelForm):

    latitude = forms.CharField(required=False)
    longitude = forms.CharField(required=False)

    class Meta:
        model = PointOfInterest
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'required': 'true'}),
            'alt_name': forms.TextInput(),
            'description': forms.Textarea(attrs={'required': 'true'}),
            'history': forms.Textarea(attrs={'required': 'true'}),
            'facts': forms.Textarea(attrs={'required': 'true'}),
            'street': forms.TextInput(attrs={'required': 'false'}),
            'city': forms.TextInput(attrs={'required': 'false'}),
            'state': forms.TextInput(attrs={'required': 'false'}),
            'zip': forms.TextInput(attrs={'required': 'false'}),
            'contact_name': forms.TextInput(attrs={'required': 'true'})
        }

class HazardForm(forms.ModelForm):

    class Meta:
        model = Hazard
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'required': 'true'}),
            'description': forms.Textarea(attrs={'required': 'true'})
        }


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = []
        widgets = {
            'caption': forms.TextInput(attrs={'required': 'true'}),
            'name': forms.TextInput(attrs={'required': 'true'})
        }


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        exclude = []
        widgets = {
            'caption': forms.TextInput(attrs={'required': 'true'}),
            'name': forms.TextInput(attrs={'required': 'true'})
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = []
        widgets = {
            'category': forms.TextInput(attrs={'required': 'true'})
        }
