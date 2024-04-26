from django.db import models
from django.contrib.auth.models import User


def profile_photo_upload_to(instance, filename):
    return f"profile_photos/user_{instance.user.id}/{filename}"


def post_photos_upload_to(instance, filename):
    return f"post_photos/user_{instance.profile.user.id}/{filename}"


class Profile(models.Model):
    choices = [('M', 'Male'),
               ('F', 'Female'),
               ('O', 'Others')]

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='user_profile')
    profile_photo = models.ImageField(upload_to=profile_photo_upload_to, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=4, choices=choices, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    following = models.ManyToManyField(to=User, related_name='following')
    followers = models.ManyToManyField(to=User, related_name='followers')

    class Meta:
        db_table = 'profile'


class Post(models.Model):
    profile = models.ForeignKey(to=Profile, related_name='profile_post', on_delete=models.CASCADE)
    post_photo = models.ImageField(upload_to=post_photos_upload_to, blank=True, null=True)
    is_video = models.BooleanField(default=False)
    caption = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(to=Profile)

    class Meta:
        db_table = 'post'
        ordering = ['-date_added']