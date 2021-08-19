from django import forms
from .models import Participant
  

class ParticipantsForm(forms.ModelForm):
    name = forms.CharField(label='Name',
                            max_length=70,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.EmailField(label='Email',
                            max_length=100,
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    class Meta:
        model = Participant
        fields = "__all__"
