from django.test import TestCase, Client, tag, RequestFactory, utils
from .models import Profile, get_user_model, UserOpenid
from .views import UserViewSet
# Create your tests here.


class ProfileTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='bob', password='123456')
        self.c = Client()
        self.c.force_login(self.user)
        self.factory = RequestFactory()

    def test_user_signal(self):
        profile = self.user.profile
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.user.username, 'bob')

    @tag('fast')
    def test_client(self):
        response = self.c.get('/user/api/v1/users/statistics/')
        self.assertEqual(response.status_code, 200)

