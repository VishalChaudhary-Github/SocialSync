from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from profile_app.models import Profile


def login_form(request):
    return render(request, 'login.html')


def user_authentication(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))
    else:
        messages.error(request, 'Enter the correct username or password')
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def register_form(request):
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


def landing(request):
    return render(request, 'landing.html')


def about_us(request):
    return render(request, 'about_us.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('landing-page'))