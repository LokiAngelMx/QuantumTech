from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Ingresa un email válido.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_.',
            'password1': 'Tu contraseña no puede ser similar a tu otra información personal.',
            'password2': 'Ingresa la misma contraseña de antes, para verificación.',
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class PasswordUpdateForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label="Nueva contraseña", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmar nueva contraseña", required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data