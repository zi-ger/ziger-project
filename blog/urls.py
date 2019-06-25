from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like', views.post_like, name='post_like'),
    path('people/', views.people, name='people'),
    path('help/', views.help, name='help'),
    path('help/message_sent', views.message_sent, name='message_sent'),
    path('follow_unfollow', views.follow_unfollow, name='follow_unfollow'),
    path('u/<slug:username>/', views.user, name='user'),

]