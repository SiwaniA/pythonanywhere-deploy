from django import forms
from . models import BlogModel

class Edit_Blog(forms.ModelForm):
    class Meta:
        model=BlogModel
        fields=('title','content')