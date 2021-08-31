from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from draw.models import Participant 

@receiver(post_save, sender=User)
def create_firstParticipat(sender, instance, created, **kwargs):
    if created:
        Participant.objects.create(name=instance.username, 
                                    email=instance.email, 
                                    user=instance).save()
        


