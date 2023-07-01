from django import forms

from orders.models import ShippingInformation, PaymentDetails


class ShippingInformationForm(forms.ModelForm):
    class Meta:
        model = ShippingInformation
        fields = '__all__'


class PaymentDetailsForm(forms.ModelForm):
    class Meta:
        model = PaymentDetails
        fields = '__all__'
