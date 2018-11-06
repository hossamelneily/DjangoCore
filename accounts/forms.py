from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, login
from django.db.models import Q

User = get_user_model()

class LoginForm(forms.Form):
    query = forms.CharField(max_length=255,label='UserName/Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


    def clean(self,*arg,**kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')


        user = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        )
        print(user)
        # user = authenticate(username=username,password=password)
        if not user.exists():
            raise forms.ValidationError("Invalid credentials")

        if not user.first().check_password(password):
            raise forms.ValidationError("Invalid credentials-- password incorrect")
        self.cleaned_data['user_obj']=user.first()
        return super().clean(*arg,**kwargs)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]