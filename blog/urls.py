from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like', views.post_like, name='post_like'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    # url('user_login/$', views.user_login, name='user_login'),
    url('logout/$', views.user_logout, name='logout'),
    url(r'^follow_unfollow$', views.follow_unfollow, name='follow_unfollow'),
    url(r'^users/(?P<username>\w{0,30})/$', views.users, name='users'),

]