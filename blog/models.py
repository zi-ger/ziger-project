from django.conf import settings
from django.utils import timezone
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class UserPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    
    text = models.CharField(max_length = 512)
    created_at = models.DateTimeField(default=timezone.now)
    
    likes = models.ManyToManyField(User, blank=True, related_name='liked')

    replys = models.IntegerField(default=0)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')
    
    def __str__(self):
        return "{} - {}".format(self.user, self.created_at)

    class Meta:
        ordering = ('-created_at',)