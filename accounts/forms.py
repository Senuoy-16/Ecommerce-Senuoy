from django import forms
from .models import Account

class RegisterForm(forms.ModelForm):

    password           = forms.CharField(widget=forms.PasswordInput)    
    confirmed_password = forms.CharField(widget=forms.PasswordInput)    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country']
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password           = cleaned_data.get('password')
        confirmed_password = cleaned_data.get('confirmed_password')
        
        if password and confirmed_password and password != confirmed_password:
            raise forms.ValidationError("Your password didn't match.")
        return cleaned_data


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Your email adress'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Your phone number'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['confirmed_password'].widget.attrs['placeholder'] = 'Confirm your password'




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'country', 'email']
        widgets = {
            'country': forms.Select(choices=Account.get_country())
        }
 






