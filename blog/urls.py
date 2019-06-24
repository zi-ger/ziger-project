from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like', views.post_like, name='post_like'),
    path('social/', views.social, name='social'),
    path('help/', views.help, name='help'),
    path('help/message_sent', views.message_sent, name='message_sent'),
    url(r'^follow_unfollow$', views.follow_unfollow, name='follow_unfollow'),
    url(r'^u/(?P<username>\w{0,50})/$', views.user, name='user'),

]