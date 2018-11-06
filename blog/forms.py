from django import forms
from .models import PostModel
from django.core.validators import ValidationError


class PostalForm(forms.ModelForm):
    class Meta:

        model=PostModel
        fields=[
            'title',
            'content'
        ]
        labels = {
            'title':'this is new label for title',
            'view_count': 'here is new label for view_count'
        }
        # help_texts = {
        #     'title':'please put you title'
        # }
        error_messages = {
            "title":{
                'max_length':'must have certain number of characters!!',
                "required":"this title is required",
            }
        }

    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['title'].error_messages = {
    #             'required':'this title is required'
    #         }

        # by for loop
        # for field in self.fields.values():
        #     field.error_messages = {
        #         'required':'this {field_name} is required'.format(field_name=field.lable)
        #     }
    # def save(self, commit=True):
    #     form = super().save(commit=False)
    #     form.view_count = 100
    #     if commit:
    #         form.save()
    #     return form

INT_CHS = tuple((x,x) for x in range(1,20))

class Postaltest(forms.Form):
    username = forms.CharField(label='User Name',widget=forms.TextInput())
    age= forms.IntegerField(initial=7,widget=forms.Select(choices=INT_CHS))
    email = forms.EmailField()


    def __init__(self,*args,**kwargs):
        age = kwargs.pop('age',None)   ## automatic if there is kwargs , django will create a data variable and iniate it with the kwargs dictioanry
        print(kwargs)
        print(args)
        super().__init__(*args,**kwargs)
        if age:
            self.fields['age'].initial=age


    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 10:
            raise ValidationError("age below 10")
        return age

