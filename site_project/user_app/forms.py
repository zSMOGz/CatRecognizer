from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта')
    image = forms.ImageField(label='Аватар')

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2',
                  'image']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта')

    class Meta:
        model = User
        fields = ['username',
                  'email']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(label='Аватар')

    class Meta:
        model = Profile
        fields = ['image']
