from food.models import CustomUser, Feedback
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import re

class NewUserForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True, help_text='Enter your Sabanci email address')
    phone_number = forms.CharField(max_length=15, required=True, help_text='Phone number must have the format 05xxx')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']
        help_texts = {
            'password1': None,
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if the email matches the "username@sabanciuniv.edu" format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@sabanciuniv\.edu$', email):
            raise forms.ValidationError("Email must be in the format 'username@sabanciuniv.edu'.")

        return email

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, help_text='Enter the OTP sent to your email')

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')

        # Get the user from the request
        user = self.request.user

        # Check if the user's profile has an OTP set
        if not user.profile.otp:
            raise forms.ValidationError("No OTP has been generated for this user. Please register or request a new OTP.")

        # Check if the entered OTP matches the one in the user's profile
        if otp != user.profile.otp:
            raise forms.ValidationError("Invalid OTP. Please check your email for the correct OTP.")

        return otp
    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'feedback']