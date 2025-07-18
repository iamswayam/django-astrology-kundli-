from django.contrib import admin
from django import forms
from django_flatpickr.widgets import DatePickerInput, TimePickerInput
from .models import KundliDetails

class KundliDetailsForm(forms.ModelForm):
    birth_date = forms.DateField(widget=DatePickerInput())
    birth_time = forms.TimeField(widget=TimePickerInput())

    class Meta:
        model = KundliDetails
        fields = '__all__'

@admin.register(KundliDetails)
class KundliDetailsAdmin(admin.ModelAdmin):
    form = KundliDetailsForm
    list_display = ('name', 'gender', 'birth_date', 'place_of_birth', 'birth_time')
    search_fields = ('name', 'place_of_birth')
    readonly_fields = ('timezone',)