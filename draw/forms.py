from django import forms
from .models import Participant
  

class ParticipantsForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"