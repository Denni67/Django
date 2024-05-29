from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    date_of_birth = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    mobile_number = forms.CharField(max_length=15, help_text='Required. Enter your mobile number')

    class Meta:
        model = User
        fields = ['username', 'email', 'date_of_birth', 'mobile_number', 'password1', 'password2']
    

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User

# forms.py

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'mobile_number','address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
