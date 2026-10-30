from django.test import TestCase
from django.urls import reverse, resolve

from ..views import signup
from ..forms import SignUpForm

from django.contrib.auth.models import User

# Create your tests here.
class SignupPageTests(TestCase):
    def setUp(self):
        url=reverse('signup')
        self.response=self.client.get(url)

    def test_signup_view_status_code(self):
        url=reverse('signup')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup')
        self.assertEqual(view.func, signup)
    
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',
            'email':'john.example@gmail.com'
        }
        self.response = self.client.post(url, data)
        self.index_url = reverse('index')

    def test_redirection(self):
        self.assertRedirects(self.response, self.index_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.index_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_form_inputs(self):
        redirect_response=self.client.get(reverse('signup'))
        self.assertContains(redirect_response, '<input', 5)
        self.assertContains(redirect_response, 'type="text"', 1)
        self.assertContains(redirect_response, 'type="email"', 1)
        self.assertContains(redirect_response, 'type="password"', 2)