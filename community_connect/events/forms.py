from django import forms
from django.contrib.auth.models import User
from .models import Profile, Event, Feedback
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from datetime import date
from .models import Event
import re


class VolunteerSignupForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email Address")
    phone_number = forms.CharField(
        max_length=15, required=True, label="Phone Number"
    )
    captcha = CaptchaField()  # Add captcha to the form

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Regular expression to validate email
        pattern = r'^[^@]+@[^@]+\.[^@]+$'
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format. Please provide a valid email address.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
            # Update the profile with role and phone number
            Profile.objects.filter(user=user).update(
                role='Volunteer',
                phone_number=self.cleaned_data['phone_number']
            )
        return user

# Add this missing EventForm class
class EventForm(forms.ModelForm):
    captcha = CaptchaField()  # Add CAPTCHA field

    class Meta:
        model = Event
        fields = ['name', 'description', 'date']

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date <= date.today():
            raise ValidationError("The event date must be in the future.")
        return selected_date

class FeedbackForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Feedback
        fields = ['event', 'feedback']  # Match the fields in the Feedback model