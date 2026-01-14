from django.test import TestCase
from apps.users.models import User


class UserModelTestCase(TestCase):
    """Test cases for User model"""

    def test_user_creation(self):
        """Test creating a user"""
        user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'Test User')
        self.assertEqual(user.email, 'test@example.com')
