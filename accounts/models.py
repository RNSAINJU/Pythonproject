from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location=models.CharField(max_length=30, blank=True)
    birth_date=models.CharField(max_length=12, blank=True)
    email_confirmed=models.BooleanField(default=False)
    image=models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
