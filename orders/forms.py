from django import forms
from .models import Order
from django.core.exceptions import ValidationError

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']


    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder']  = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder']   = 'Enter your last name'
        self.fields['email'].widget.attrs['placeholder']       = 'Your email adress'
        self.fields['address'].widget.attrs['placeholder']      = 'Address of your residence'
        self.fields['postal_code'].widget.attrs['placeholder'] = 'Postal Code'
        self.fields['city'].widget.attrs['placeholder']        = 'City'
              




