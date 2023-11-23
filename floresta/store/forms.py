from django import forms


class CartForm(forms.Form):
    shipper = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={"class": "select-delivery"}),
        required=True
    )
    order_comment = forms.CharField(
        widget=forms.Textarea(attrs={"class": "additional-comment", "rows": 5, "cols": 35}),
        max_length=300,
        required=False
    )


class CheckoutForm(forms.Form):
    name = forms.CharField(
        min_length=1,
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Twoje imię...', 'autofocus': True}),
        label="Imię",
        required=True
    )
    last_name = forms.CharField(
        min_length=1,
        max_length=80,
        widget=forms.TextInput(attrs={'placeholder': 'Twoje nazwisko...'}),
        label="Nazwisko",
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'jan.kowalski@example.com'}),
        label="Adres e-mail",
        required=True
    )
    street = forms.CharField(
        min_length=1,
        max_length=80,
        widget=forms.TextInput(attrs={'placeholder': 'ul. Wrocławska 13/34'}),
        label="Ulica",
        required=True
    )
    city = forms.CharField(
        min_length=1,
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Wrocław'}),
        label="Miasto",
        required=True
    )
    postal_code = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '00-000'}),
        label="Kod pocztowy",
        max_length=10,
        required=True
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '000-111-222'}),
        label="Numer telefonu (opcjonalne)",
        max_length=20,
        required=False
    )
