from django import forms
from .models import PostModel



class PostalForm(forms.ModelForm):
    class Meta:

        model=PostModel
        fields=[
            'title',
            'content'
        ]