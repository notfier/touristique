from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from data.tests.factories import DepartmentFactory
from registration.models import User

from ..models import Department


class TestDepartment(APITestCase):

    def setUp(self):
        self.department_one = DepartmentFactory()
        self.department_two = DepartmentFactory()
        user = User.objects.create(first_name='Bo', last_name='Devchik', email='bohdan@gmail.com')
        token_key = Token.objects.get(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token_key))

    def test_unauthorized_user(self):
        # sign out
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.get(reverse('data-get-departments'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('detail'),
            'Authentication credentials were not provided.'
        )

    def test_get_departments_list(self):
        response = self.client.get(reverse('data-get-departments'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn(self.department_two.address, str(response.content))
        self.assertIn(self.department_one.name, str(response.content))


class TestDepartmentInfo(APITestCase):

    def setUp(self):
        self.department_one = DepartmentFactory()
        user = User.objects.create(first_name='Bo', last_name='Devchik', email='bohdan@gmail.com')
        token_key = Token.objects.get(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token_key))

    def test_unauthorized_user(self):
        # sign out
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.get(reverse('data-get-department'), data={
            'department_pk': self.department_one.pk
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('detail'),
            'Authentication credentials were not provided.'
        )

    def test_get_department_info(self):
        response = self.client.get(reverse('data-get-department'), data={
            'department_pk': self.department_one.pk
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.department_one.name, str(response.content))
        self.assertIn(self.department_one.address, str(response.content))

    def test_change_department_info(self):
        response = self.client.put(reverse('data-get-department'), data={
            'department_pk': self.department_one.pk,
            'phone': '777777',
            'address': 'Carrer de l\'Avenir',
            'name': self.department_one.name,
            'zip_code': self.department_one.zip_code
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('777777', str(response.content))
        self.assertIn('Carrer de l\'Avenir', str(response.content))

    def test_create_department(self):
        response = self.client.post(reverse('data-get-department'), data={
            'phone': '777777',
            'address': 'Carrer de l\'Avenir',
            'name': 'Parabola',
            'zip_code': '77777'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('777777', str(response.content))
        self.assertIn('Carrer de l\'Avenir', str(response.content))
        self.assertIn('Parabola', str(response.content))
        self.assertEqual(Department.objects.count(), 2)
