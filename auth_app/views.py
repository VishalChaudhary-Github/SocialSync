import secrets
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from profile_app.models import Profile
from redis import Redis
from .task import send_email
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

server = Redis(decode_responses=True)


def landing(request):
    return render(request, 'landing.html')


def about_us(request):
    return render(request, 'about_us.html')


def login_form(request):
    if request.user.is_authenticated:
        return HttpResponse("User needs to be logged out to access this page!")
    return render(request, 'login.html')


def user_authentication(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))
    else:
        messages.error(request, 'Enter a correct username or password')
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def register_form(request):
    if request.user.is_authenticated:
        return HttpResponse("User needs to be logged out to access this page!")
    return render(request, 'register.html')


def new_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        user = User.objects.create_user(username=username, password=password,
                                        email=email, first_name=f_name, last_name=l_name)
        Profile.objects.create(user=user)
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(redirect_to=reverse('auth_app-register'))

    else:
        messages.success(request, 'Registration Successful')
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('landing-page'))


def forgot_password(request):
    return render(request, 'forgot_password.html', context={"enter_otp": False})


def generate_otp():
    otp = ''.join([secrets.choice('0123456789') for x in range(6)])
    return otp


def sending_otp(request):
    if request.method == "POST":
        email = request.POST['email']
        otp = generate_otp()
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            messages.error(request, "Provided Email is not registered!")
            return HttpResponseRedirect(redirect_to=reverse("auth_app-forgot-password"))
        else:
            send_email.delay(recipient=email, otp=otp, username=user.get_username())
            server.setex(name=email, time=5*60, value=otp)
            messages.success(request, "OTP has been sent to the registered email.")
            return render(request, 'forgot_password.html', context={'enter_otp': True, 'user_id': user.id})
    return HttpResponseForbidden('Invalid Request')


def verify_otp(request):
    if request.method == "POST":
        uid = request.POST['uid']
        otp = request.POST['otp']
        user = User.objects.get(id=uid)
        if server.exists(user.email) == 1:
            if otp == server.get(user.email):
                messages.success(request, "Verification Successful, Enter a new password.")
                field = 'enter_password'
            else:
                messages.error(request, "Incorrect OTP, Try Again.")
                field = 'enter_otp'
            return render(request, 'forgot_password.html', context={field: True, 'user_id': user.id})
        else:
            messages.error(request, "OTP has expired!")
            return HttpResponseRedirect(redirect_to=reverse("auth_app-forgot-password"))
    return HttpResponseForbidden('Invalid Request')


def set_new_password(request):
    if request.method == "POST":
        password = request.POST['password']
        user = User.objects.get(id=request.POST['uid'])
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))
    return HttpResponseForbidden('Invalid Request')


@csrf_exempt
def social(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)
    except ValueError:
        return HttpResponseForbidden()
    email = user_data['email']
    name = user_data['name']

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(username=email.split('@')[0],
                                        password='',
                                        email=email,
                                        first_name=name.split(' ')[0],
                                        last_name=name.split(' ')[1])
        Profile.objects.create(user=user)
    login(request, user)
    return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))
