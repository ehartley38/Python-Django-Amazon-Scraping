from django import forms
from .models import Item, TrackingDetails

class ItemSearchForm(forms.Form):
    url = forms.CharField()


    '''
    class Meta:
        model = Item
        fields = ['name']'''

class ItemTrackingForm(forms.ModelForm):
    class Meta:
        model = TrackingDetails
        fields = ['target_price']