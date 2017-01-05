from django.test import TestCase

from data.tests.factories import DepartmentFactory

from .factories import TouristFactory, TouristCardFactory


class TestTouristModel(TestCase):

    def test_unicode_and_full_name_method(self):
        tourist = TouristFactory()
        self.assertEqual(
            str(tourist),
            '{0} {1}'.format(tourist.first_name, tourist.last_name)
        )


class TestTouristCardModel(TestCase):

    def test_unicode_method(self):
        dep = DepartmentFactory()
        tourist = TouristFactory()
        tourist_card = TouristCardFactory(
            current_department=dep,
            tourist=tourist
        )
        self.assertEqual(
            str(tourist_card),
            '{0}\'s card'.format(tourist)
        )
