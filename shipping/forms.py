from django import forms
from django.utils.translation import gettext_lazy as _
from shipping.models import ShippingAddress, ShippingMethod

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'first_name', 'last_name', 'company', 'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country', 'phone'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': _('First Name')
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': _('Last Name')
            }),
            'company': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': _('Company (optional)')
            }),
            'address_line1': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': _('Street Address')
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': _('Apartment, suite, etc.')
            }),
            'city': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': _('City')
            }),
            'state': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': _('State/Province')
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': _('Postal Code')
            }),
            'country': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': _('Phone Number')
            }),
        }

class ShippingMethodForm(forms.Form):
    shipping_method = forms.ModelChoiceField(
        queryset=ShippingMethod.objects.none(),
        empty_label=None,
        widget=forms.RadioSelect(attrs={
            'class': 'form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out'
        })
    )

    def __init__(self, *args, available_methods=None, **kwargs):
        super().__init__(*args, **kwargs)
        if available_methods is not None:
            self.fields['shipping_method'].queryset = available_methods