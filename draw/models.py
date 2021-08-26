from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.name}: {self.email}'

