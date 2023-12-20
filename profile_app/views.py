from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from profile_app.models import Profile, Post
from django.contrib.auth.models import User


def feeds(request):
    if request.user.is_authenticated:
        context = {'profile_photo': request.user.user_profile.profile_photo,
                   'full_name': request.user.get_full_name()}

        filtered_post = []
        for post in Post.objects.all():
            if post.profile.user in request.user.user_profile.following.all():
                filtered_post.append(post)

        context['filtered_post'] = filtered_post

        if request.user.user_profile.description is not None:
            context['description'] = request.user.user_profile.description

        return render(request, 'feed.html', context=context)
    else:
        return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def home(request):
    if request.user.is_authenticated:
        context = {'username': request.user.get_username(),
                   'profile_photo': request.user.user_profile.profile_photo,
                   'full_name': request.user.get_full_name(),
                   'all_posts': request.user.user_profile.profile_post.all(),
                   'following': request.user.user_profile.following.all(),
                   'followers': request.user.user_profile.followers.all()}

        if request.user.user_profile.description is not None:
            context['description'] = request.user.user_profile.description
        else:
            context['description'] = ('The more we value things outside our control, '
                                      'the less control we have.')

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
    if request.method == 'POST':
        profile_photo_ = request.FILES.get('profile_photo')
        description_ = request.POST['description']
        gender_ = request.POST['gender']
        dob_ = request.POST['dob']

        profile = Profile.objects.get(user=request.user)

        profile.description = description_
        profile.gender = gender_
        profile.dob = dob_

        if profile_photo_:
            profile.profile_photo = profile_photo_

        profile.save()

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


def like_post(request):
    _id = request.POST['pid']
    post = Post.objects.get(id=_id)
    prf = Profile.objects.get(user=request.user.pk)
    post.likes.add(prf)
    return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))