from django.test import TestCase, tag
from django.urls import reverse
from django.contrib.auth.models import User
from django_dynamic_fixture import G


class SignupViewTestCase(TestCase):

    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        self.wrong_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'otherpassword123',
        }


    def test_signup_successsful(self):
        response = self.client.post(reverse('signup'), self.valid_data)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertEqual(response.status_code, 302)


    def test_signup_invalid(self):
        msg = "<li>The two password fields didn"
        response = self.client.post(reverse('signup'), self.wrong_data)
        self.assertContains(response, msg)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertEqual(response.status_code, 200)


class LoginViewTests(TestCase):

    def setUp(self):

        self.user = G(
            User,
            username='testuser',
            email='testuser@mail.com',
            password='testpassword123',
        )

    @tag('login')
    def test_login_successful(self):
        response = self.client.post(reverse('login'), {
            'username': self.user.username,
            'password': self.user.password,
        })

        self.user.refresh_from_db()
        print(response.content)
        self.assertEqual(response.status_code, 200)
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)


    def test_login_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    @tag('login')
    def test_logout(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(response.status_code, 302)
