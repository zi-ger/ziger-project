from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    follows = models.ManyToManyField(   'self', #self reference
                                        related_name='followed_by', #facilitate searches
                                        symmetrical=False) #like twitter, followers are not unilateral
    def __str__(self):
        return self.username