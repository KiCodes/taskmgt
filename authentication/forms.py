from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserImage

class SignUpForm(UserCreationForm):

    class Meta:
        # we specify the django authentication model 'User' as opposed to using creating a custom User model 
        # the fields we wish to specify from the model have to be written the same was as in AbstractUser Model class which User class inherits from
        # to specify all fields of User Model use fields = '__all__'
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['image']

