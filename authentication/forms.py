from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

