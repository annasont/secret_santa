from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length = 70)
    email = models.EmailField()

    def __str__(self):
        return self.name
