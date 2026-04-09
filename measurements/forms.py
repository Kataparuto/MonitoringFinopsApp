from django import forms
from .models import CostRecord

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = CostRecord
        fields = ['project', 'service', 'amount', 'region']
