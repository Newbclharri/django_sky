from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile, UserSpirit, WingedLight
from django.forms import ModelForm
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        
class EditProfileForm(UserChangeForm):
        
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
class SpiritForm(ModelForm):
    class Meta:
        model = UserSpirit
        fields = ['description', 'name']
        
# class AddWingedLightForm(forms.ModelForm):
#     class Meta:
#         model = WingedLight
#         fields = ('wingedlight','realm','location')
    
    