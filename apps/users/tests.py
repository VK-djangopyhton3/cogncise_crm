from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


# Create your tests here.


class UserTest(TestCase):

    def setUp(self):
        user_a = User(email='testuser1@test.com', phone='12345', name='testuser1')
        user_a.is_staff = True
        user_a.is_verified = True
        user_a.is_superuser = True
        user_a.set_password = 'somepassword'
        user_a.save()

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 2)
