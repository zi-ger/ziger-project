from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4

def upload_rename(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        return 'profile_images/{}/{}.{}'.format(instance.pk, uuid4().hex, ext)
    else:
        pass

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to=upload_rename, blank=True, default='profile_images/none/default.png')
    bio = models.CharField(null=True, blank=True, max_length = 512)
    follows = models.ManyToManyField(   'self', #self reference
                                        related_name='followed_by', #facilitate searches
                                        symmetrical=False) #like twitter, followers are not unilateral
    def __str__(self):
        return self.username