

from email.headerregistry import Address
from http import client
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_OPTIONS = (
    ('Efectivo', 'cash'),
    ('Electronico', 'on-line')
)

class CheckoutForm(forms.Form):
    client = forms.CharField()
    cedula = forms.IntegerField()
    phone = forms.IntegerField()
    Address = forms.ChoiceField()
    city = forms.CharField()
    payment = forms.ChoiceField(choices=PAYMENT_OPTIONS)
    stamp_start = forms.DateTimeField()


class CouponForm(forms.Form):
        code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))