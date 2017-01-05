from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from data.tests.factories import DepartmentFactory
from registration.models import User
from tourists.models import Tourist, TouristCard


class TestTouristInfo(APITestCase):

    def setUp(self):
        user = User.objects.create(
            first_name='Bo',
            last_name='Devchik',
            email='bohdan@gmail.com'
        )
        token_key = Token.objects.get(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token_key))

        self.tourist = Tourist.objects.create(
            first_name='Jamie',
            last_name='Hince',
            email='jamie@kills.co.uk'
        )

    def test_unauthorized_user(self):
        # sign out
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(reverse('tourists-info', args=[self.tourist.pk]))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('detail'),
            'Authentication credentials were not provided.'
        )

    def test_get_tourist_info(self):
        response = self.client.get(reverse('tourists-info', args=[self.tourist.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), self.tourist.first_name)
        self.assertEqual(response.data.get('last_name'), self.tourist.last_name)
        self.assertEqual(response.data.get('id'), self.tourist.id)

    def test_update_tourist_info(self):
        response = self.client.put(reverse('tourists-info', args=[self.tourist.pk]), data={
            'first_name': 'Bruce',
            'last_name': self.tourist.last_name,
            'email': 'hacked@anonymous.net'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.tourist.id)
        self.assertEqual(Tourist.objects.get(pk=self.tourist.pk).first_name, 'Bruce')

    def test_wrong_updated_data(self):
        response = self.client.put(reverse('tourists-info', args=[self.tourist.pk]), data={
            'first_name': self.tourist.first_name,
            'last_name': self.tourist.last_name,
            'email': 'incorrect_email'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], 'Enter a valid email address.')


class TestTouristCardInfo(APITestCase):

    def setUp(self):
        user = User.objects.create(first_name='Bo', last_name='Devchik', email='bohdan@gmail.com')
        token_key = Token.objects.get(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token_key))

        self.tourist = Tourist.objects.create(
            first_name='Killian',
            last_name='Murphy',
            email='killian@lala.irl'
        )
        self.department = DepartmentFactory()
        self.second_department = DepartmentFactory()
        self.tourist_card = TouristCard.objects.create(
            tourist=self.tourist,
            current_department=self.department
        )

    def test_unauthorised_user(self):
        # sign out
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(reverse('tourists-card-info'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('detail'),
            'Authentication credentials were not provided.'
        )

    def test_get_tourist_card_info(self):
        response = self.client.get(reverse('tourists-card-info'), data={
            'tourist_card_pk': self.tourist_card.pk.hex
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('tourist').get('first_name'), self.tourist.first_name)
        self.assertEqual(response.data.get('card_id'), self.tourist_card.card_id.hex)

    def test_update_tourist_info(self):
        response = self.client.put(
            reverse('tourists-card-info'),
            data={
                'tourist_card_pk': self.tourist_card.pk.hex,
                'tourist': {
                    'first_name': 'Bruce',
                    'last_name': self.tourist.last_name,
                    'email': 'hacked@anonymous.net'
                },
                'current_department': self.second_department.pk
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('card_id'), self.tourist_card.card_id.hex)
        self.assertEqual(
            TouristCard.objects.get(pk=self.tourist_card.card_id.hex).tourist.first_name,
            'Bruce'
        )

    def test_create_new_tourist_card_info(self):
        response = self.client.post(reverse('tourists-card-info'), data={
            'tourist': {
                'first_name': 'Tom',
                'last_name': 'Hardy',
                'email': 'thomas@hardy.co.uk'
            },
            'current_department': self.department.pk
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('tourist').get('last_name'), 'Hardy')
        self.assertIn(self.department.address, str(response.content))
