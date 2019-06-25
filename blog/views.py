from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from .forms import UserPostForm, ReplyForm, HelpForm
from .models import UserPost

import logging

User = get_user_model()
# logger = logging.getLogger('django.request')

@login_required
def index(request):
    following_user_ids = []
    following_user_ids.append(request.user.id)

    for fol in request.user.follows.all():
        following_user_ids.append(fol.id)

    userposts = UserPost.objects.filter(user__in=following_user_ids)

    replies = []
    for up in userposts:
        replies += up.replies.all()

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

@login_required
def user(request, username=''):
    try:
        puser = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    userposts = UserPost.objects.filter(user=puser.id)
    replies = []
    for up in userposts:
        replies += up.replies.all()

    if username == User.objects.get(id=request.user.id).username:
        return render(request, 'blog/user.html', {'puser': puser, 'userposts': userposts, 'replies': replies, })
    else:
        
        reqU = User.objects.get(id=request.user.id)
        following = reqU.follows.all()

        if puser in following:
            return render(request, 'blog/user.html', {'puser': puser, 'userposts': userposts, 'replies': replies, 'follow': True, })
        else:
            return render(request, 'blog/user.html', {'puser': puser, 'userposts': userposts, 'replies': replies, 'follow': False, })

@login_required
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

@login_required
def follow_unfollow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        user = User.objects.get(id=follow_id)

        reqU = User.objects.get(id=request.user.id)
        following = reqU.follows.all()

        if user in following:
            reqU.follows.remove(user)
        else:
            reqU.follows.add(user)

        return redirect('u/{}'.format(user.username))

@login_required
def post_delete(request, pk):
    post = get_object_or_404(UserPost, id=pk)
    if post.user.id == request.user.id:
        post.delete()
    return redirect('/')

@login_required
def post_like_pl(request, pk):        
    post = get_object_or_404(UserPost, id=pk)

    likes = post.likes.all()

    if request.user in likes:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('/')

@login_required
def post_like(request, pk):
    try:
        post = get_object_or_404(UserPost, id=pk)
        likes = post.likes.all()

        if request.user in likes:
            post.likes.remove(request.user)
            data = {
                'likesCount': post.likes.count(),
                'liked': False,
                'status': 1
            }
        else:
            post.likes.add(request.user)
            data = {
                'likesCount': post.likes.count(),
                'liked': True,
                'status': 1
            }
        
    except:
        data = {
            'status': 0
        }

    return JsonResponse(data)

def people(request):
    user_list = User.objects.all()
    return render(request, 'blog/people.html', {'user_list': user_list})

def help(request):
	if request.method == 'GET':
		email_form = HelpForm()
	else:
		email_form = HelpForm(request.POST)
		if email_form.is_valid():
			subject = email_form.cleaned_data['subject']
			message = email_form.cleaned_data['message']
			sender = email_form.cleaned_data['sender']

			try:
				send_mail(sender+' - '+subject, message, from_email=sender, recipient_list=['ziger.application@gmail.com'])
			except BadHeaderError:
				return HttpResponse("Error.")
			return redirect('message_sent')
	return render(request, 'blog/help.html', {'form': email_form})

def message_sent(request):
      messages.success(request, 'Message sent.')
      return redirect('index')