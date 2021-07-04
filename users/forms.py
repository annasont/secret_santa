from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django.utils.translation import ugettext_lazy as _

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    password1 = forms.CharField(
        label='Hasło',
        strip=False,
        widget=forms.PasswordInput(),
        help_text='Twoje hasło musi zawierać co najmniej 8 znaków.\nTwoje hasło nie może być zbyt popularne.\nTwoje hasło nie może składać się wyłącznie z cyfr.'
    )
    password2 = forms.CharField(
        label='Powtórz hasło',
        widget=forms.PasswordInput(),
        strip=False,
        help_text='Wprowadź takie same hasło jak powyżej.',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Imię',
        }
        help_texts = {
            'username': 'Maksymalnie 150 znaków. Używaj wyłącznie liter, cyfr oraz @/./+/-/_.'
        }
