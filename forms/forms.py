from django import forms
from myspa.models import MassageTherapist, Position, Salon, SpaUser, TypeCategories
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
      
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Name'}))
    phone = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone', 'type': 'tel'}))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    profile_image = forms.ImageField(label='', widget=forms.FileInput(attrs={'class': 'create_image'}), required=False)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input','placeholder': 'Confirm password'}))

    class Meta:
        model = SpaUser
        fields = ('username', 'phone', 'email', 'password1', 'password2', 'profile_image')
        
    def save(self):
        user = super().save(commit=False)
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image
        user.save()
        return user
        
        
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Name'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))
  
    class Meta:
        model = SpaUser
        fields = ('username', 'password')
        

class MassageTherapistForm(forms.ModelForm):
    salon = forms.ModelChoiceField(queryset=Salon.objects.all(), label='', widget=forms.Select(attrs={'class': 'form-input'}))
    position = forms.ModelMultipleChoiceField(queryset=Position.objects.all(), label='', widget=forms.SelectMultiple(attrs={'class': 'form-input select', 'size': '10'}))

    class Meta:
        model = MassageTherapist
        fields = ('salon', 'position')
        
        