from django.test import TestCase

from ..models import User


class TestUserModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name='Joshua',
            middle_name='Brad',
            last_name='Kiddings',
            email='jo@raw_stromg.com'
        )

    def test_unicode_and_get_full_name_methods(self):
        self.assertEqual(str(self.user), '{0} {1} {2}'.format(
            self.user.first_name,
            self.user.middle_name,
            self.user.last_name
        ))

    def test_get_short_name_method(self):
        self.assertEqual(
            self.user.get_short_name(),
            self.user.first_name
        )
