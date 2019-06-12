# from django.contrib.auth.models import User
from django.conf import settings
# from users.models import CustomUser
from django.utils import timezone
from django.db import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     follows = models.ManyToManyField(   'self', #self reference
#                                         related_name='followed_by', #facilitate searches
#                                         symmetrical=False) #like twitter, followers are not unilateral 

#     def __unicode__(self):
#         return self.user.username

# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0]) #got from ahackersday.
#                                                                                     #this creates a UserProfile when
#                                                                                     #an user creates an account

class UserPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    
    text = models.CharField(max_length = 512)
    created_at = models.DateTimeField(default=timezone.now)
    
    likes = models.IntegerField(default=0)
    replys = models.IntegerField(default=0)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')
    
    def __str__(self):
        return "{} - {}".format(self.user, self.created_at)

    class Meta:
        ordering = ('-created_at',)