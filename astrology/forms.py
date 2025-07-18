from django import forms
from .models import KundliDetails

class KundliDetailsUserForm(forms.ModelForm):
    class Meta:
        model = KundliDetails
        fields = ['name', 'gender', 'birth_date', 'birth_time', 'place_of_birth']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['birth_time'].widget = forms.TimeInput(attrs={'type': 'time'})