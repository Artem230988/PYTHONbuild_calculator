from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from calculator.models import *


class PreparationTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='Geralt',
            password='test'
        )
        self.user2 = User.objects.create_user(username='Ciri')
        self.customer_1 = Customers.objects.create(
            last_name='Гость',
            first_name='Гость',
            phone='789456123',
            manager=self.user1
        )
        self.customer_2 = Customers.objects.create(
            last_name='Человек',
            first_name='Человечеще',
            phone='789456123',
            manager=self.user1
        )
        self.customer_3 = Customers.objects.create(
            last_name='Тело',
            first_name='Живое',
            phone='789456123',
            manager=self.user2
        )
        self.customer_4 = Customers.objects.create(
            last_name='Тело',
            first_name='Не очень',
            phone='789456123',
            manager=self.user2
        )
        self.client_1 = APIClient()
        self.client_2 = APIClient()
        self.client_1.force_authenticate(user=self.user1)
        self.client_2.force_authenticate(user=self.user2)


class CustomerTest(PreparationTests):
    def test_customer_all(self):
        """Вывод всех Заказчиков."""
        request = self.client_1.get('/api/v1/customers/', format='json')
        self.assertEqual(len(request.data), 2)
        self.assertEqual(request.data[0]['manager'], 'Geralt')
        self.assertNotEqual(request.data[1]['manager'], 'Ciri')

    def test_customer_one(self):
        """Вывод конкретного заказчика."""
        request = self.client_1.get(
            f'/api/v1/customers/{self.customer_2.id}/', format='json'
        )
        self.assertEqual(request.data['last_name'], 'Человек')
        self.assertEqual(request.data['first_name'], 'Человечеще')
        self.assertEqual(request.data['manager'], 'Geralt')

    def test_customer_post(self):
        """Добавление нового заказчика."""
        data = {
            'last_name': 'Новый',
            'first_name': 'Новейший',
            'phone': '7894561231'
        }
        request = self.client_1.post(
            '/api/v1/customers/', data=data, format='json'
        )
        new_customer = Customers.objects.get(last_name='Новый')
        self.assertEqual(new_customer.first_name, 'Новейший')
        self.assertEqual(new_customer.manager, self.user1)

    def test_customer_patch(self):
        """Изменение данных заказчика."""
        data = {
            'last_name': 'Новая фамилия'
        }
        request = self.client_1.patch(
            f'/api/v1/customers/{self.customer_1.id}/',
            data=data,
            format='json'
        )
        customer = Customers.objects.get(pk=self.customer_1.id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(customer.last_name, 'Новая фамилия')
        request = self.client_1.patch(
            f'/api/v1/customers/{self.customer_4.id}/',
            data=data,
            format='json'
        )
        customer = Customers.objects.get(pk=self.customer_4.id)
        self.assertEqual(request.status_code, 404)
        self.assertNotEqual(customer.last_name, 'Новая фамилия')

    def test_customer_delete(self):
        """Изменение данных заказчика."""
        customers_before = len(Customers.objects.all())
        request = self.client_1.delete(
            f'/api/v1/customers/{self.customer_1.id}/', format='json'
        )
        customers_after = len(Customers.objects.all())
        self.assertEqual(request.status_code, 204)
        self.assertEqual(customers_before, customers_after + 1)
        request = self.client_1.delete(
            f'/api/v1/customers/{self.customer_3.id}/', format='json'
        )
        customers_check = len(Customers.objects.all())
        self.assertEqual(request.status_code, 404)
        self.assertEqual(customers_check, customers_after)
