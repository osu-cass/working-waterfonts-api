import django.forms as forms
from working_waterfronts.working_waterfronts_api.models import Hazard


class HazardForm(forms.ModelForm):

    class Meta:
        model = Hazard
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'required': 'true'}),
            'description': forms.Textarea(attrs={'required': 'true'})
        }
