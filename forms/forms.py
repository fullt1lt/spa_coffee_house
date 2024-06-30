from django import forms
from myspa.models import MassageTherapist, Position, Review, Salon, SpaUser, SpaСategories
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError  
    
class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label="Iм'я", widget=forms.TextInput(attrs={'class': 'form-input-name', 'placeholder': "Iм'я"}))
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-input-name', 'placeholder': "Прізвище"}))
    phone = forms.CharField(label='Телефон',widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Телефон', 'type': 'tel'}))
    email = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'E-mail'}))
    profile_image = forms.ImageField(label='', widget=forms.FileInput(attrs={'class': 'create_image'}), required=False)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Повторіть пароль", widget=forms.PasswordInput(attrs={'class': 'form-input','placeholder': "Повторіть пароль"}))

    class Meta:
        model = SpaUser
        fields = ('first_name', 'last_name', 'phone', 'email', 'password1', 'password2', 'profile_image')

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.email = self.cleaned_data['email']
        
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image

        if commit:
            user.save()
        return user
        

class LoginUserForm(AuthenticationForm):
    email = forms.EmailField(label='Ваш e-mail', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Ваш e-mail', 'id': 'id_email_2'}))
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
        
        
class CategoriesUpdateForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'create_name', 'placeholder': 'Name'}))
    categories_image = forms.ImageField(label='', widget=forms.FileInput(attrs={'class': 'create_categories_image'}), required=False)
    description = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'create_description', 'rows': 8, 'placeholder': 'Description'}))

    class Meta:
        model = SpaСategories
        fields = ('categories_image', 'name', 'description')
        

class CategoriesAddForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'add_create_name', 'placeholder': 'Назва категорії'}), required=True)
    categories_image = forms.ImageField(label='', widget=forms.FileInput(attrs={'class': 'add_create_categories_image'}), required=True)
    description = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'add_create_description', 'rows': 8, 'placeholder': 'Опис категорії'}), required=True)

    class Meta:
        model = SpaСategories
        fields = ('categories_image', 'name', 'description')
        
        
class MassageTherapistUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=100, required=True)
    last_name = forms.CharField(label='Last Name', max_length=100, required=True)
    position = forms.ModelMultipleChoiceField(queryset=Position.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-input select', 'size': '4'}))
    profile_image = forms.ImageField(label='Profile Image', required=False)

    class Meta:
        model = MassageTherapist
        fields = ['first_name', 'last_name', 'position', 'profile_image']


# class MassageTherapistUpdateForm(forms.ModelForm):
#     first_name = forms.CharField(label='First Name', max_length=100, required=True)
#     last_name = forms.CharField(label='Last Name', max_length=100, required=True)
#     position = forms.ModelMultipleChoiceField(queryset=Position.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-input select', 'size': '4'}))
#     profile_image = forms.ImageField(label='Profile Image', required=False)

#     class Meta:
#         model = MassageTherapist
#         fields = ['first_name', 'last_name', 'position', 'profile_image']