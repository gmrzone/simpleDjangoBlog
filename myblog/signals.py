from django.contrib.auth.models import User, Group   # User And Group Model
from django.db.models.signals import post_save        # Signals
from django.dispatch import receiver                  # Signal Connecting Decorator
from .models import Profile                           # Importing our Profile Model Because We AHve To Create A Profile For User
               

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(full_name=instance.username, user=instance, gender='male', slug=instance.username) # Creating USer Profile
        default_group = Group.objects.get(name='beginner')
        instance.groups.add(default_group) 
