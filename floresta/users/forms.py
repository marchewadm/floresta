from django import forms
from custom_user.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        min_length=1,
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Twoje imię...', 'autofocus': True}),
        label="Jak się nazywasz?"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'jan.kowalski@example.com'}),
        error_messages={'unique': 'Podany adres e-mail jest już w użyciu.'},
        label="Adres e-mail"
    )
    password1 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': '********'}),
        label="Hasło"
    )
    password2 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': '********'}),
        label="Powtórz hasło"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Hasła nie są identyczne.", code='password_mismatch')

        return password2

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')
