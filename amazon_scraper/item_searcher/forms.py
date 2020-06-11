from django import forms
from .models import Item

class ItemSearchForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['name']
