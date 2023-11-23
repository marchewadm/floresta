from django import forms


class CartForm(forms.Form):
    shipper = forms.ChoiceField(choices=[], widget=forms.Select(attrs={"class": "select-delivery"}), required=True)
    order_comment = forms.CharField(widget=forms.Textarea(attrs={"class": "additional-comment", "rows": 5, "cols": 35}), max_length=300, required=False)
