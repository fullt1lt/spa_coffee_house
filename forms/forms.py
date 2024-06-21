from django import forms
from myspa.models import MassageTherapist, Position, Review, Salon, SpaUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError  
    
class RegisterUserForm(UserCreationForm):
    name = forms.CharField(label="Iм'я", widget=forms.TextInput(attrs={'class': 'form-input-name', 'placeholder': "Iм'я"}))
    surname = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-input-name', 'placeholder': "Прізвище"}))
    phone = forms.CharField(label='Телефон',widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Телефон', 'type': 'tel'}))
    email = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'E-mail'}))
    profile_image = forms.ImageField(label='', widget=forms.FileInput(attrs={'class': 'create_image'}), required=False)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Повторіть пароль", widget=forms.PasswordInput(attrs={'class': 'form-input','placeholder': "Повторіть пароль"}))

    class Meta:
        model = SpaUser
        fields = ('name', 'surname', 'phone', 'email', 'password1', 'password2', 'profile_image')

    def save(self):
        user = super().save(commit=False)
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image
        user.save()
        return user
        

class LoginUserForm(AuthenticationForm):
    email = forms.EmailField(label='Ваш e-mail', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Ваш e-mail'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()  # Скрываем поле username
        self.fields['username'].required = False

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password")
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class MassageTherapistForm(forms.ModelForm):
    salon = forms.ModelChoiceField(queryset=Salon.objects.all(), label='', widget=forms.Select(attrs={'class': 'form-input'}))
    position = forms.ModelMultipleChoiceField(queryset=Position.objects.all(), label='', widget=forms.SelectMultiple(attrs={'class': 'form-input select', 'size': '10'}))

    class Meta:
        model = MassageTherapist
        fields = ('salon', 'position')
        

class ReviewForm(forms.ModelForm):
    therapist = forms.ModelChoiceField(queryset=MassageTherapist.objects.all(), empty_label="Выберите массажиста")
    rating = forms.IntegerField(widget=forms.HiddenInput(), required=False, min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Review
        fields = ['therapist', 'rating', 'comment']
        
    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')

        if rating is None:
            raise forms.ValidationError("Пожалуйста, выберите рейтинг")