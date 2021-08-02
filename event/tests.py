from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, time
from django.utils.timezone import make_aware

from authentication.models import UserProfile
from event.models import UserEvent, Country, PublicHoliday
from event.service import send


def get_api_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


class EventTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='test_user1',
            email='test_user1@mail.ru',
            password='test_user1'
        )
        self.user2 = User.objects.create_user(
            username='test_user2',
            email='test_user2@mail.ru',
            password='test_user2'
        )
        self.event11 = UserEvent.objects.create(
            user=self.user1,
            name='event11',
            start_date='2021-12-31T17:45:00Z',
            end_date='2021-12-31T17:47:00Z',
            reminder_before=24)
        self.event12 = UserEvent.objects.create(
            user=self.user1,
            name='event12',
            start_date='2021-12-30T17:48:00Z',
            end_date='2021-12-30T18:47:00Z',
            reminder_before=2)
        self.event13 = UserEvent.objects.create(
            user=self.user1,
            name='event13',
            start_date='2021-12-29T17:45:00Z',
            end_date='2021-12-29T17:47:00Z',
            reminder_before=1)
        self.event21 = UserEvent.objects.create(
            user=self.user2,
            name='event21',
            start_date='2021-12-31T17:45:00Z',
            end_date='2021-12-31T17:47:00Z',
            reminder_before=24)
        self.event22 = UserEvent.objects.create(
            user=self.user2,
            name='event22',
            start_date='2021-12-30T17:48:00Z',
            end_date='2021-12-30T18:47:00Z',
            reminder_before=2)
        self.event23 = UserEvent.objects.create(
            user=self.user2,
            name='event23',
            start_date='2021-12-29T17:45:00Z',
            end_date='2021-12-29T17:47:00Z',
            reminder_before=1)

    def test_event_create1(self):
        url = reverse('create_event')
        data = {
            "name": "тестирование",
            "start_date": "2021-12-31T17:40:00Z",
            "end_date": "2021-12-31T23:59:59.999999Z"
        }
        client = get_api_client(self.user1)
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['start_date'], data['start_date'])
        self.assertEqual(response.data['end_date'], data['end_date'])

    def test_event_create2(self):
        url = reverse('create_event')
        data = {
            "name": "тестирование",
            "start_date": "2021-12-31T17:40:00Z"
        }
        client = get_api_client(self.user1)
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['start_date'], data['start_date'])
        event = UserEvent.objects.get(**data)
        end_date = make_aware(datetime.combine(event.start_date, time.max))
        self.assertEqual(event.end_date, end_date)

    def test_event_editing_get(self):
        url = reverse('event', kwargs={'id_event': self.event12.id})
        client = get_api_client(self.user1)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_event_editing_put(self):
        url = reverse('event', kwargs={'id_event': self.event12.id})
        data = {
            "name": "event12 new",
            "start_date": "2021-12-30T17:48:00Z",
            "end_date": "2021-12-30T18:47:00Z",
            "reminder_before": 2
        }
        client = get_api_client(self.user1)
        response = client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['start_date'], data['start_date'])
        self.assertEqual(response.data['end_date'], data['end_date'])

    def test_event_editing_patch(self):
        url = reverse('event', kwargs={'id_event': self.event13.id})
        data = {
            "name": "event13 new",
        }
        client = get_api_client(self.user1)
        response = client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data['name'], data['name'])

    def test_event_editing_delete(self):
        url = reverse('event', kwargs={'id_event': self.event13.id})
        client = get_api_client(self.user1)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)

    def test_all_user_event(self):
        url = reverse('all_events')
        client = get_api_client(self.user1)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(len(response.data), len(UserEvent.objects.filter(user_id=self.user1.id)))

    def test_event_of_day(self):
        url = reverse('events_of_day', kwargs={'day': 30, 'month': 12, 'year': 2021})
        client = get_api_client(self.user2)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data[0]['name'], self.event22.name)
        self.assertEqual(response.data[0]['start_date'], self.event22.start_date)

    def test_events_of_month(self):
        url = reverse('events_of_month', kwargs={'month': 12, 'year': 2021})
        client = get_api_client(self.user2)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(len(response.data), 31)
        self.assertEqual(response.data[28]['events'][0]['start_date'], self.event23.start_date)
        self.assertEqual(response.data[28]['events'][0]['name'], self.event23.name)
        self.assertEqual(response.data[29]['events'][0]['start_date'], self.event22.start_date)
        self.assertEqual(response.data[29]['events'][0]['name'], self.event22.name)
        self.assertEqual(response.data[30]['events'][0]['start_date'], self.event21.start_date)
        self.assertEqual(response.data[30]['events'][0]['name'], self.event21.name)


class PublicHolidayTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user1',
            email='test_user1@mail.ru',
            password='test_user1'
        )
        self.country = Country.objects.create(
            name='Belarus'
        )
        self.profile1 = UserProfile.objects.create(
            user=self.user,
            phone='+375295556256',
            first_name='Kate',
            Last_name='Zablotskaya',
            country=self.country,
            gender='f'
        )
        self.holiday = PublicHoliday.objects.create(
            country=self.country,
            name='Belarus: Christmas Day (Catholic)',
            start_date='2021-12-25T00:00:00Z',
            end_date='2021-12-26T00:00:00Z'
        )

    def test_public_holiday(self):
        url = reverse('public_holiday', kwargs={'month': 12, 'year': 2021})
        client = get_api_client(self.user)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.holiday.name)
        self.assertEqual(response.data[0]['start_date'], self.holiday.start_date)


class TestAuthenticationForEventsMethods(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='test_user1',
            email='test_user1@mail.ru',
            password='test_user1'
        )
        self.user2 = User.objects.create_user(
            username='test_user2',
            email='test_user2@mail.ru',
            password='test_user2'
        )
        self.event11 = UserEvent.objects.create(
            user=self.user1,
            name='event11',
            start_date='2021-12-31T17:45:00Z',
            end_date='2021-12-31T17:47:00Z',
            reminder_before=24)
        self.event12 = UserEvent.objects.create(
            user=self.user1,
            name='event12',
            start_date='2021-12-30T17:48:00Z',
            end_date='2021-12-30T18:47:00Z',
            reminder_before=2)
        self.event13 = UserEvent.objects.create(
            user=self.user1,
            name='event13',
            start_date='2021-12-29T17:45:00Z',
            end_date='2021-12-29T17:47:00Z',
            reminder_before=1)
        self.event21 = UserEvent.objects.create(
            user=self.user2,
            name='event21',
            start_date='2021-12-31T17:45:00Z',
            end_date='2021-12-31T17:47:00Z',
            reminder_before=24)
        self.event22 = UserEvent.objects.create(
            user=self.user2,
            name='event22',
            start_date='2021-12-30T17:48:00Z',
            end_date='2021-12-30T18:47:00Z',
            reminder_before=2)
        self.event23 = UserEvent.objects.create(
            user=self.user2,
            name='event23',
            start_date='2021-12-29T17:45:00Z',
            end_date='2021-12-29T17:47:00Z',
            reminder_before=1)

    def test_event_create1(self):
        url = reverse('create_event')
        data = {
            "name": "тестирование",
            "start_date": "2021-12-31T17:40:00Z",
            "end_date": "2021-12-31T23:59:59.999999Z"
        }
        client = APIClient()
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_create2(self):
        url = reverse('create_event')
        data = {
            "name": "тестирование",
            "start_date": "2021-12-31T17:40:00Z"
        }
        client = APIClient()
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_editing_get(self):
        url = reverse('event', kwargs={'id_event': self.event12.id})
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_editing_put(self):
        url = reverse('event', kwargs={'id_event': self.event12.id})
        data = {
            "name": "event12 new",
            "start_date": "2021-12-30T17:48:00Z",
            "end_date": "2021-12-30T18:47:00Z",
            "reminder_before": 2
        }
        client = APIClient()
        response = client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_editing_patch(self):
        url = reverse('event', kwargs={'id_event': self.event13.id})
        data = {
            "name": "event13 new",
        }
        client = APIClient()
        response = client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_editing_delete(self):
        url = reverse('event', kwargs={'id_event': self.event13.id})
        client = APIClient()
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_user_event(self):
        url = reverse('all_events')
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_of_day(self):
        url = reverse('events_of_day', kwargs={'day': 30, 'month': 12, 'year': 2021})
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_events_of_month(self):
        url = reverse('events_of_month', kwargs={'month': 12, 'year': 2021})
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SendEmail(APITestCase):


    def test_send_email(self):
        #send('katrin.z.94@mail.ru')
        url = reverse('send_email')
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
