from django.test import TestCase

from .factories import DepartmentFactory
from ..serializers import DepartmentSerializer


class TestTouristSerializer(TestCase):

    def test_correct_serialized_data(self):
        department = DepartmentFactory()
        serialized = DepartmentSerializer(department)
        # check correct fields including
        self.assertEqual(serialized.data.get('id'), department.id)
        self.assertEqual(serialized.data.get('name'), department.name)
        self.assertEqual(serialized.data.get('zip_code'), department.zip_code)
        self.assertEqual(serialized.data.get('address'), department.address)

    def test_serializing_received_data(self):
        data = {
            'name': 'Rogue',
            'address': 'Rogue One street 6',
            'phone': '123434556',
            'zip_code': '453634'
        }
        serialized = DepartmentSerializer(data=data)
        self.assertTrue(serialized.is_valid())
