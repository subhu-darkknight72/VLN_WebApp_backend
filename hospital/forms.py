from django import forms
from .models import actionHistory

class performActionForm(forms.ModelForm):
    class Meta:
        model = actionHistory
        fields = ('action', 'observation')
        # specify the fields to be displayed in the form
        fields = ['action']

        