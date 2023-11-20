from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from profile_app.models import Profile, Post


def feeds(request):
    if request.user.is_authenticated:
        context = {'profile_photo': request.user.user_profile.profile_photo,
                   'full_name': request.user.get_full_name(),
                   'description': request.user.user_profile.description,
                   'followings': request.user.user_profile.following.all()}
        return render(request, 'feed.html', context=context)
    else:
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def home(request):
    if request.user.is_authenticated:
        context = {'username': request.user.get_username(),
                   'profile_photo': request.user.user_profile.profile_photo,
                   'full_name': request.user.get_full_name(),
                   'description': request.user.user_profile.description,
                   'gender': request.user.user_profile.get_gender_display(),
                   'dob': request.user.user_profile.dob,
                   'all_posts': request.user.user_profile.profile_post.all()}
        return render(request, 'home.html', context=context)
    else:
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def settings(request):
    if request.user.is_authenticated:
        context = {'first_name': request.user.first_name,
                   'last_name': request.user.last_name,
                   'email': request.user.email,
                   'username': request.user.get_username()}
        return render(request, 'settings.html', context=context)
    else:
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def update_profile(request):
    profile_photo_ = request.FILES.get('profile_photo')
    description_ = request.POST['description']
    gender_ = request.POST['gender']
    dob_ = request.POST['dob']
    if profile_photo_ is None:
        p = Profile.objects.filter(user=request.user.pk).update(description=description_, gender=gender_, dob=dob_)
    else:
        p = Profile.objects.filter(user=request.user.pk).update(profile_photo=profile_photo_, description=description_,
                                                                gender=gender_, dob=dob_)

    return HttpResponseRedirect(redirect_to=reverse('profile_app-home'))


def add_post(request):
    image = request.FILES.get('image')
    caption = request.POST['caption']
    pro_ = Profile.objects.get(user=request.user.pk)
    Post.objects.create(profile=pro_, post_photo=image, caption=caption)

    return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))