from django.urls import path
from auth_app.views import login_form, register_form, user_authentication, new_user, logout_user

urlpatterns = [
    path('login', login_form, name='auth_app-login'),
    path('register', register_form, name='auth_app-register'),
    path('user-authentication', user_authentication, name='auth_app-user-authentication'),
    path('new-user', new_user, name='auth_app-new-user'),
    path('logout', logout_user, name='auth_app-logout')
]