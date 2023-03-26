from django import forms
from .models import Student

class AttendanceForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label='Present students'
    )

    def __init__(self, class_, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = class_.students.all()
