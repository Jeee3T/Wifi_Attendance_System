from django import forms
from django.forms import formset_factory
from .models import AttendanceForm


class AttendanceFormForm(forms.ModelForm):
    class Meta:
        model = AttendanceForm
        fields = ('status',)

AttendanceFormFormSet = formset_factory(AttendanceFormForm, extra=0)
