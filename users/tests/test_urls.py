from django.test import SimpleTestCase
from django.urls import resolve, reverse
from challenges.views import index_view, challenge_detail_view, mountain_detail_view, achievement_edit_view

from users.views import profile_view
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

    def test_login_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_profile_resolves(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile_view)