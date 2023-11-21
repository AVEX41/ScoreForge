from django.test import TestCase
from django.urls import reverse

from .models import User

# Create your tests here.


class IndexTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")

    def test_first(self):
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
