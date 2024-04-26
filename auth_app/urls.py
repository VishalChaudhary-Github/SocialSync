from django.urls import path
from auth_app.views import (login_form, register_form, user_authentication, new_user,
                            logout_user, forgot_password, sending_otp, verify_otp, set_new_password, social)


urlpatterns = [
    path('login/', login_form, name='auth_app-login'),
    path('register/', register_form, name='auth_app-register'),
    path('user-authentication/', user_authentication, name='auth_app-user-authentication'),
    path('new-user/', new_user, name='auth_app-new-user'),
    path('logout/', logout_user, name='auth_app-logout'),
    path("forgot-password/", forgot_password, name='auth_app-forgot-password'),
    path("sending-otp/", sending_otp, name='auth_app-sending-otp'),
    path("verify-otp/", verify_otp, name="auth_app-verify-otp"),
    path("set-new-password/", set_new_password, name='auth_app-set-new-password'),
    path("social/", social, name='auth_app-sign-in-with-google')
]