from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from profile_app.models import Profile, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages


def paginated_results(user_obj, num):
    x = Post.objects.filter(profile__user__in=user_obj.user_profile.following.all())
    p = Paginator(x, 3)
    return p.page(num)


def feeds(request):
    if request.user.is_authenticated:
        page_num = request.GET.get('page', default=1)
        context = {'profile_photo': request.user.user_profile.profile_photo,
                   'full_name': request.user.get_full_name()}

        current_page = paginated_results(request.user, page_num)
        context['current_page'] = current_page
        if len(current_page.object_list) == 0:
            context['is_list_empty'] = True

        if request.user.user_profile.description is not None:
            context['description'] = request.user.user_profile.description
        return render(request, 'feed.html', context=context)
    return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def posts_restructured(user_obj):
    posts = list(user_obj.user_profile.profile_post.all())
    b = [tuple(posts[i:i + 3]) for i in range(0, len(posts), 3)]
    return b


def home(request):
    if request.user.is_authenticated:
        context = {'username': request.user.get_username(),
                   'profile_photo': request.user.user_profile.profile_photo,
                   'full_name': request.user.get_full_name(),
                   'all_posts': posts_restructured(request.user),
                   'following': request.user.user_profile.following.all(),
                   'followers': request.user.user_profile.followers.all()}

        if request.user.user_profile.description is not None:
            context['description'] = request.user.user_profile.description

        return render(request, 'home.html', context=context)
    return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def settings(request):
    if request.user.is_authenticated:
        context = {'first_name': request.user.first_name,
                   'last_name': request.user.last_name,
                   'email': request.user.email,
                   'username': request.user.get_username()}
        return render(request, 'settings.html', context=context)
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
    return HttpResponseForbidden(content='Invalid response')


def validate_post(name: str):
    extension = name.split('.')[1]
    if extension in ('jpg', 'png'):
        video = False
        return video
    elif extension in ('mp4', 'mov', 'avi', 'wmv'):
        video = True
        return video
    else:
        raise NameError('Improper File Format!')


def add_post(request):
    if request.method == "POST":
        try:
            image = request.FILES.get('image')
            is_video = validate_post(image.name)
            caption = request.POST['caption']
            Post.objects.create(profile=request.user.user_profile, post_photo=image, caption=caption, is_video=is_video)
        except Exception as e:
            messages.error(request, f"{e}")
        else:
            messages.success(request, "Post Created Successfully!")
        return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))
    return HttpResponseForbidden(content='Invalid response')


def search_user(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.GET['user']
            all_users = User.objects.filter(username__icontains=user)
            context = {'users': all_users,
                       'self': request.user.user_profile.following.all()}
            return render(request, 'search_list.html', context=context)
        return HttpResponseForbidden(content='Invalid response')
    return HttpResponseRedirect(redirect_to=reverse('auth_app-login'))


def follow_user(request):
    if request.method == "POST":
        if request.POST['username'] != request.user.get_username():
            usr = User.objects.get(username=request.POST['username'])
            usr.user_profile.followers.add(request.user)
            request.user.user_profile.following.add(usr)
        return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))
    return HttpResponseForbidden(content='Invalid response')


def unfollow_user(request):
    if request.method == "POST":
        usr = User.objects.get(username=request.POST['username'])
        usr.user_profile.followers.remove(request.user)
        request.user.user_profile.following.remove(usr)
        return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))
    return HttpResponseForbidden(content='Invalid response')


def like_post(request):
    if request.method == 'POST':
        _id = request.POST['pid']
        post = Post.objects.get(id=_id)
        post.likes.add(request.user.user_profile)
        return HttpResponseRedirect(redirect_to=reverse('profile_app-feeds'))
    return HttpResponseForbidden(content='Invalid response')


def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        try:
            post = Post.objects.get(id=post_id)
        except Exception as e:
            return HttpResponseForbidden("Invalid Request")
        else:
            post.delete()
            return HttpResponseRedirect(redirect_to=reverse('profile_app-home'))
    return HttpResponseForbidden("Invalid response")

