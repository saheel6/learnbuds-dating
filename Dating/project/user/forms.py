from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customuser, Employee, Jobseeker,PersonalInfo ,AdditionalInfo, UserMedia # Replace with your actual Customuser model import



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": 'Email', 
            'class': 'form-control', 
            'autocomplete': 'off'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": 'Username', 
            'class': 'form-control', 
            'autocomplete': 'off'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": 'Password', 
            'class': 'form-control', 
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": 'Confirm Password', 
            'class': 'form-control', 
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = Customuser
        fields = ['email', 'username', 'password1', 'password2']

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })
            
            if field_name == 'bio':
                field.widget.attrs.update({
                    'rows': 4,
                })
        
        self.fields['DOB'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
        
        
        
class AdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = AdditionalInfo
        exclude=['user']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling or attributes to fields if needed
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Example classes for styling
            })




class UserMediaForm(forms.ModelForm):
    class Meta:
        model = UserMedia
        exclude=['user']
        widgets = {
            'additional_image1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_image2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_image3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_image4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_image5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'short_reel': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude=['user']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling or attributes to fields if needed
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Example classes for styling
            })


class JobseekerForm(forms.ModelForm):
    class Meta:
        model = Jobseeker
        fields = ['title','expertise_level']     
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling or attributes to fields if needed
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Example classes for styling
            })