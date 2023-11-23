from django.urls import path
from profile_app.views import (home, feeds, settings, update_profile, add_post, search_user,
                               follow_user, new_password, view_user, like_post, unfollow_user)

urlpatterns = [
    path('feeds', feeds, name='profile_app-feeds'),
    path('home', home, name='profile_app-home'),
    path('settings', settings, name='profile_app-settings'),
    path('update-profile', update_profile, name='profile_app-update-profile'),
    path('add-post', add_post, name='profile_app-add-post'),
    path('search-user', search_user, name='profile_app-search-user'),
    path('follow-user/<slug:user_name>', follow_user, name='profile_app-follow-user'),
    path('set-password', new_password, name='profile_app-set-password'),
    path('view-user/<slug:user_name>', view_user, name='profile_app-view-user'),
    path('like-post', like_post, name='profile_app-like-post'),
    path('unfollow-user/<slug:user_name>', unfollow_user, name='profile_app-unfollow-user')
]