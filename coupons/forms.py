from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CouponApplyForm, self).__init__(*args, **kwargs)

        self.fields['code'].widget.attrs['placeholder'] = 'Enter coupon code'