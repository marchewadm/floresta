from django.contrib.auth.forms import UserCreationForm
from custom_user.models import User
from django import forms


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Twoje imię...'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'jan.kowalski@example.com'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********'}))

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')
