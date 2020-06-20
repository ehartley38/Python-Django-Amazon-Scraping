from django import forms
from .models import Item

class ItemSearchForm(forms.Form):
    url = forms.CharField()


    '''
    class Meta:
        model = Item
        fields = ['name']'''
