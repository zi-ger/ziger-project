from .models import UserPost#, User
from django import forms
from django.conf import settings



class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('text',)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('text', 'parent')
    
# class UserLoginForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta():
#         model = User
#         fields = ('username','password','email')