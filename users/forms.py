from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'photo',
            'email',
            'first_name',
            'last_name',
            'bio',
            'password'

        )