from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import *


# Create your tests here.
class PageTestCase(TestCase):
    fixtures = ['bpacking_bike.json', 'bpacking_category.json', 'bpacking_tags.json', 'bpacking_auth_user.json']

    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('bpacking/index.html', response.template_name)
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        w = Bike.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        print(w) 

    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        w = Bike.published.all().select_related('cat')
        self.assertQuerysetEqual(response.context_data['posts'], w[(page-1)*paginate_by:page*paginate_by])

    def test_content_post(self):
        w = Bike.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)


    def tearDown(self):
        "Действия после выполнения каждого теста"

class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'mil',
            'email': 'mil@mil.ru',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }

        self.user_model = get_user_model()

    def test_form_registration_get(self):
        path = reverse('register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_registration_success(self):

        path = reverse('register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(self.user_model.objects.filter(username=self.data['username']).exists())

    def test_user_registration_password_error(self):
        self.data['password2'] = '12345678A'
        path = reverse('register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Введенные пароли не совпадают.")

    def test_user_registration_user_exists_error(self):
        self.user_model.objects.create(username=self.data['username'])
        path = reverse('register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Пользователь с таким именем уже существует.")
