from django import forms
from .models import ManufacturerOrProductSeller, MachineVendor, ProfessionalWorker, CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
      model = CustomUser
      fields = ['username','password','user_type']

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = ManufacturerOrProductSeller
        fields = ['phone_number', 'company_name', 'gst_certificate',
                  'pan_card_company', 'pan_card_owner', 'aadhar_card',
                  'bank_details']

class MachineVendorForm(forms.ModelForm):
    class Meta:
        model = MachineVendor
        fields = ['phone_number', 'aadhar_card', 'pan_card', 'gst_details',
                 'bank_details']

class ProfessionalWorkerForm(forms.ModelForm):
    class Meta:
        model = ProfessionalWorker
        fields = ['phone_number', 'category', 'aadhar_card', 'pan_card',
                 'gst_details', 'bank_details']

class UserTypeLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, widget=forms.Select)