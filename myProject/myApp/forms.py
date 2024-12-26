

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# added for email 
from django import forms
from .models import Review


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#added for email 
# myApp/forms.py


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Adjust these fields based on your Review model
