from django import forms

from .models import *
from datetime import date
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

STATUS_CHOICES= [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('excuse', 'Excuse')
    ]

class AttendanceForm(forms.Form):

    reference = forms.CharField(required=True)
    status = forms.CharField(label='Trainee Status', widget=forms.Select(choices=STATUS_CHOICES))

    class Meta:
        model = AttendanceRecord
        fields = ('status')

    def clean_reference(self):
        reference = self.cleaned_data['reference']
        trainee_by_ref = Trainee.objects.filter(reference=reference)

        if not trainee_by_ref.exists():
            raise forms.ValidationError("This reference code doesn't exist. Please supply a different one.")

        return reference


    # def save(self, commit=True):
    #     attendance = super(AttendanceForm, self).save(commit=False)
    #     trainee = Trainee.objects.get(reference=self.cleaned_data['reference'])
    #     attendance.trainee = trainee
    #     attendance.status = self.cleaned_data['status']
    #     attendance.group = trainee.group
    #     # user.email = self.cleaned_data['email']
    #     if commit:
    #         attendance.save()
    #     return attendance