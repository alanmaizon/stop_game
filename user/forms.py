from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from .models import User

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("This email is not registered.")
        return email
    
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserProfileUpdateForm(forms.ModelForm):
    avatar = forms.ChoiceField(choices=User.AVATAR_CHOICES, widget=forms.Select(attrs={'class': 'hidden-avatar-field'}))

    class Meta:
        model = User
        fields = ['avatar','email']

