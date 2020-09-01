from django.test import SimpleTestCase
from django.urls import resolve, reverse
from challenges.views import index_view, challenge_detail_view, mountain_detail_view, achievement_edit_view

class TestUrls(SimpleTestCase):

    def test_index_chall_resolves(self):
        url = reverse('index_chall')
        self.assertEquals(resolve(url).func, index_view)

    def test_detail_chall_resolves(self):
        url = reverse('detail_chall', args=['challenge-name'])
        self.assertEquals(resolve(url).func, challenge_detail_view)

    def test_detail_mnt_resolves(self):
        url = reverse('detail_mnt', args=['challenge-name', 'mountain-name'])
        self.assertEquals(resolve(url).func, mountain_detail_view)
    
    def test_achievement_edit_resolves(self):
        url = reverse('achievement_edit', args=['challenge-name', 'mountain-name'])
        self.assertEquals(resolve(url).func, achievement_edit_view)

