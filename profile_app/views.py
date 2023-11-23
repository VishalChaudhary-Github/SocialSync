from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from profile_app.models import Profile, Post
from django.contrib.auth.models import User


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
                   'all_posts': request.user.user_profile.profile_post.all(),
                   'following': request.user.user_profile.following.all(),
                   'followers': request.user.user_profile.followers.all()}
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


def search_user(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.GET['user']
            all_users = User.objects.filter(username__startswith=user)
            context = {'users': all_users,
                       'self': request.user.user_profile.following.all()}
            return render(request, 'search_list.html', context=context)
        else:
            return HttpResponseForbidden(content='Invalid response')
    else:
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def follow_user(request, user_name):
    if request.user.is_authenticated:
        if user_name != request.user.get_username():
            usr = User.objects.get(username=user_name)
            usr.user_profile.followers.add(request.user)
            request.user.user_profile.following.add(usr)
        return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))
    else:
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def unfollow_user(request, user_name):
    if request.user.is_authenticated:
        usr = User.objects.get(username=user_name)
        usr.user_profile.followers.remove(request.user)
        request.user.user_profile.following.remove(usr)
        return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))
    else:
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def new_password(request):
    if request.user.is_authenticated:
        usr = User.objects.get(id=request.user.pk)
        new_psd = request.POST['new_password']
        usr.set_password(new_psd)
        usr.save()
        return HttpResponseRedirect(redirect_to=reverse('profile_app-settings'))
    else:
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def view_user(request, user_name):
    if request.user.is_authenticated:
        usr = User.objects.get(username=user_name)
        context = {'username': usr.get_username(),
                   'profile_photo': usr.user_profile.profile_photo,
                   'full_name': usr.get_full_name(),
                   'description': usr.user_profile.description,
                   'gender': usr.user_profile.gender,
                   'dob': usr.user_profile.dob}
        return render(request, 'view_profile.html', context=context)


def like_post(request):
    _id = request.POST['pid']
    post = Post.objects.get(id=_id)
    prf = Profile.objects.get(user=request.user.pk)
    post.likes.add(prf)
    return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))