from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index_chall'),
    path('<challenge_name>/', views.challenge_detail_view, name='detail_chall'),
    path('<challenge_name>/<mnt_name>/', views.mountain_detail_view, name='detail_mnt'),
]