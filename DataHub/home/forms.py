from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password', 'email')

class UserProfileInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].label = "Profile Picture"
        self.fields['description'].label = "Bio"

    class Meta():
         model = Profile
         fields = ('avatar', 'description')
         widgets = {
          'description': forms.Textarea(attrs={'rows':1, 'cols':50}),
         }