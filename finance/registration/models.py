from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# class MyUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     surname = models.CharField(max_length=50)
#     email = models.EmailField(max_length=50)
#     password = models.CharField(max_length=50)

    # @receiver(post_save, sender=User)
    # def update_profile_signal(sender, instance, created, **kwargs):
    #     if created:
    #         MyUser.objects.create(user=instance)
    #     instance.profile.save()