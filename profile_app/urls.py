from django.urls import path
from profile_app.views import (home, feeds, settings, update_profile, add_post, search_user,
                               follow_user, like_post, unfollow_user, delete_post)

urlpatterns = [
    path('feeds/', feeds, name='profile_app-feeds'),
    path('home/', home, name='profile_app-home'),
    path('settings/', settings, name='profile_app-settings'),
    path('update-profile/', update_profile, name='profile_app-update-profile'),
    path('add-post/', add_post, name='profile_app-add-post'),
    path('search-user/', search_user, name='profile_app-search-user'),
    path('follow-user/', follow_user, name='profile_app-follow-user'),
    path('like-post/', like_post, name='profile_app-like-post'),
    path('unfollow-user/', unfollow_user, name='profile_app-unfollow-user'),
    path("delete-post", delete_post, name='profile_app-delete-post')
]