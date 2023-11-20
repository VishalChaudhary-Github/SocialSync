from django.urls import path
from profile_app.views import home, feeds, settings, update_profile, add_post

urlpatterns = [
    path('feeds', feeds, name='profile_app-feeds'),
    path('home', home, name='profile_app-home'),
    path('settings', settings, name='profile_app-settings'),
    path('update-profile', update_profile, name='profile_app-update-profile'),
    path('add-post', add_post, name='profile_app-add-post')
]