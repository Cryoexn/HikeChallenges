from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views
from . import views

urlpatterns = [
    path('', views.index_view, name='index_chall'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile_view, name='profile'),
    path('<challenge_name>/', views.challenge_detail_view, name='detail_chall'),
    path('<challenge_name>/<mnt_name>/', views.mountain_detail_view, name='detail_mnt'),
    path('<challenge_name>/<mnt_name>/achievement_edit/', views.achievement_edit_view, name='achievement_edit'),
]