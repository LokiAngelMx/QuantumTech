from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Ingresa un email valido.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class PasswordUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Nueva contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmar nueva contraseña")

    class Meta:
        model = User
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data