from django import forms
from app.models import Database

class forms_Database(forms.ModelForm):
    class Meta:
        model=Database
        fields="__all__"