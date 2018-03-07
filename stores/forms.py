from django import forms
from stores.models import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ("name", "description")
