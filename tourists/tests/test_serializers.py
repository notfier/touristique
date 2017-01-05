# -*- coding: utf-8 -*-
from django.test import TestCase

from data.tests.factories import DepartmentFactory

from ..models import Tourist, TouristCard
from ..serializers import TouristSerializer, TouristCardSerializer
from .factories import TouristFactory, TouristCardFactory


class TestTouristSerializer(TestCase):

    def test_correct_serialized_data(self):
        tourist = TouristFactory()
        serialized = TouristSerializer(tourist)
        # check correct fields including
        self.assertEqual(serialized.data.get('id'), tourist.id)
        self.assertEqual(serialized.data.get('first_name'), tourist.first_name)
        self.assertEqual(serialized.data.get('last_name'), tourist.last_name)
        self.assertEqual(serialized.data.get('email'), tourist.email)
        self.assertTrue(serialized.data.get('date_joined'))

    def test_serializing_received_data(self):
        data = {
            'first_name': 'Alex',
            'last_name': 'Kirshner',
            'email': 'nemovlia@babyworld.com'
        }
        serialized = TouristSerializer(data=data)
        self.assertTrue(serialized.is_valid())


class TestTouristCardSerializer(TestCase):

    def setUp(self):
        self.tourist = TouristFactory()
        self.department = DepartmentFactory()
        self.tourist_card = TouristCardFactory(
            tourist=self.tourist,
            current_department=self.department
        )

    def test_correct_serialized_data(self):
        serialized = TouristCardSerializer(self.tourist_card)

        # check correct fields including
        self.assertEqual(len(serialized.data.get('card_id')), 32)
        self.assertEqual(
            serialized.data.get('tourist').get('first_name'),
            self.tourist.first_name
        )
        self.assertEqual(
            serialized.data.get('tourist').get('email'),
            self.tourist.email
        )
        self.assertEqual(
            serialized.data.get('current_department').get('name'),
            self.department.name
        )

    def test_update_received_data(self):
        data = {
            'tourist': {
                'first_name': 'Tom',
                'last_name': 'Britton',
                'email': self.tourist.email
            },
            'current_department': self.department.pk
        }
        serialized = TouristCardSerializer(self.tourist_card, data=data)
        self.assertTrue(serialized.is_valid())
        serialized.save()
        # get updated instance
        tc = TouristCard.objects.get(pk=self.tourist_card.pk)
        self.assertEqual(
            tc.tourist.first_name,
            data.get('tourist').get('first_name')
        )
        self.assertEqual(
            tc.tourist.last_name,
            data.get('tourist').get('last_name')
        )
        self.assertEqual(tc.tourist.email, self.tourist.email)

    def test_create_method_of_the_serializer(self):
        data = {
            'tourist': {
                'first_name': 'Bianca',
                'last_name': 'Mucco',
                'email': 'brionni@caravella.it'
            },
            'current_department': self.department.pk
        }
        serialized = TouristCardSerializer(data=data)
        self.assertTrue(serialized.is_valid())
        serialized.save()
        # get created instance
        tc = TouristCard.objects.get(
            tourist__email=data.get('tourist').get('email')
        )
        self.assertEqual(
            tc.tourist.first_name,
            data.get('tourist').get('first_name')
        )
        self.assertEqual(
            tc.tourist.last_name,
            data.get('tourist').get('last_name')
        )
        self.assertEqual(
            tc.tourist.email,
            data.get('tourist').get('email')
        )


