from django import forms
from .models import ShippingAdress

class ShippingAdressForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Full Name'
    }),
    required=True
    )
    shipping_email = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }),
    required=True
    )
    shipping_address1 = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address'
    }),
    required=True
    )
    shipping_address2 = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address 2'
    }),
    required=False
    )
    shipping_city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }),
    required=True
    )
    shipping_district = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'District'
    }),
    required=True
    )
    shipping_ward = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ward'
    }),
    required=True
    )
    shipping_country = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Country'
    }),
    required=True
    
    )

    class Meta:
        model = ShippingAdress
        fields = ('shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_district', 'shipping_ward', 'shipping_country')
        exclude = ('user',)

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name on Card'
    }))
    card_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Card Number'
    }))
    card_expiration = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Expiration Date'
    }))
    card_cvv = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'CVV'
    }))
    card_address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address'
    }))
    card_city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))
    card_country = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Country'
    }))