import django.forms as forms
from working_waterfronts.working_waterfronts_api.models import (Hazard, Image,
                                                                Video)


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
