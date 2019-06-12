from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model



from django.http import Http404

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from .forms import UserPostForm, ReplyForm#, UserLoginForm
from .models import UserPost#, UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

import logging

logger = logging.getLogger('django.request')

def index(request):
    if request.user.is_authenticated:

        # u = UserProfile.objects.get_or_create(user=request.user)

        following_user_ids = []
        following_user_ids.append(request.user.id)

        for fol in request.user.follows.all():
            following_user_ids.append(fol.id)
        

        userposts = UserPost.objects.filter(user__in=following_user_ids)

        # todo refazer consulta para otimizar o banco
        replies = []
        for up in userposts:
            replies += up.replies.all()

        # logger.info(replies)

        if request.method == "POST":
            pform = UserPostForm(request.POST)

            if pform.is_valid():
                post = pform.save(commit=False)
                post.user = request.user
                post.published_date = timezone.now()
                post.save()

                return redirect('/')
        else:
            pform = UserPostForm()
        return render(request, 'blog/index.html', {'pform': pform, 'posts': userposts, 'replies': replies, 'user': request.user})
    else:
        loginform = UserLoginForm(request.POST)
        return render(request, 'blog/user_login.html', {'loginform': loginform})

@login_required
def users(request, username=''):
    try:
        puser = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        raise Http404

    userposts = UserPost.objects.filter(user=puser.id)
    replies = []
    for up in userposts:
        replies += up.replies.all()

    if username == get_user_model().objects.get(id=request.user.id).username:
        return render(request, 'blog/user.html', {'puser': puser, 'userposts': userposts, 'replies': replies, })
    else:
        
        reqU = get_user_model().objects.get(id=request.user.id)
        following = reqU.follows.all()

        if puser in following:
            return render(request, 'blog/user.html', {'puser': puser, 'userposts': userposts, 'replies': replies, 'follow': True, })
        else:
            return render(request, 'blog/user.html', {'puser': puser, 'userposts': userposts, 'replies': replies, 'follow': False, })

# @login_required
def post_detail(request, pk):
    post = get_object_or_404(UserPost, id=pk)

    replies = post.replies.all()

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            post.replys += 1
            post.save()
            reply = form.save(commit=False)
            reply.user = request.user
            reply.published_date = timezone.now()
            reply.save()
            return redirect('/')
    else:
        replyForm = ReplyForm()
    return render(request, 'blog/post_detail.html', {'replyform': replyForm, 'post': post, 'replies': replies, 'user': request.user})

# @login_required
def follow_unfollow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        user = get_user_model().objects.get(id=follow_id)

        reqU = get_user_model().objects.get(id=request.user.id)
        following = reqU.follows.all()

        if user in following:
            reqU.follows.remove(user)
            logger.info('user unfollowed')
        else:
            reqU.follows.add(user)
            logger.info('user followed')

        return redirect('users/{}'.format(user.username))

# @login_required
def post_delete(request, pk):
    post = get_object_or_404(UserPost, id=pk)
    if post.user.id == request.user.id:
        post.delete()
    return redirect('/')

# @login_required
def post_like(request, pk):
    post = get_object_or_404(UserPost, id=pk)
    post.likes += 1
    post.save()
    return redirect('/')


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 return HttpResponse("Your account was inactive.")
            
#         else:
#             print("Someone tried to login and failed.")
#             print("They used username: {} and password: {}".format(username,password))
#             return HttpResponse("Invalid login details given")
#     else:
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(reverse('index'))
        
#         loginform = UserLoginForm(request.POST)
#         return render(request, 'blog/user_login.html', {'loginform': loginform})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))