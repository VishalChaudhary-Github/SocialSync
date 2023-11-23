from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    choices = [('M', 'Male'),
               ('F', 'Female'),
               ('O', 'Others')]

    user = models.OneToOneField(to=User, on_delete=models.RESTRICT, related_name='user_profile')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=4, choices=choices, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    following = models.ManyToManyField(to=User, related_name='following')
    followers = models.ManyToManyField(to=User, related_name='followers')

    class Meta:
        db_table = 'profile'


class Post(models.Model):
    profile = models.ForeignKey(to=Profile, related_name='profile_post', on_delete=models.RESTRICT)
    post_photo = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(to=Profile)

    class Meta:
        db_table = 'post'
        ordering = ['-date_added']

