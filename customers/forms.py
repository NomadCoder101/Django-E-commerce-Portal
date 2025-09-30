from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import CustomerProfile

User = get_user_model()

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text=_('Required. Enter a valid email address.')
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ('phone', 'default_currency', 'default_language', 'marketing_consent')
        
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove all non-numeric characters
            phone = ''.join(filter(str.isdigit, phone))
        return phone