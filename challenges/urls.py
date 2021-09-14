from django.urls import path
from portfolio import views as pViews
from . import views

urlpatterns = [
    path('', views.index_view, name='index_chall'),
    path('', pViews.home_view, name='portfolio_home'),
    path('<challenge_name>/', views.challenge_detail_view, name='detail_chall'),
    path('<challenge_name>/<mnt_name>/', views.mountain_detail_view, name='detail_mnt'),
    path('<challenge_name>/<mnt_name>/achievement_edit/', views.achievement_edit_view, name='achievement_edit'),
]