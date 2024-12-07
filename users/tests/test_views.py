from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task
from django.utils.timezone import now, timedelta

class HomeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            reminder_schedule=now() + timedelta(hours=2),
        )

    def test_home_authenticated_user(self):
        """Test home view for authenticated users"""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Test Task')

    def test_home_unauthenticated_user(self):
        """Test home view for unauthenticated users"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
class RegisterViewTest(TestCase):
    def test_register_success(self):
        """Test successful registration"""
        response = self.client.post(reverse('register'), {
            'fname': 'Test',
            'lname': 'User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'confirm_password': 'password',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_password_mismatch(self):
        """Test registration with password mismatch"""
        response = self.client.post(reverse('register'), {
            'fname': 'Test',
            'lname': 'User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password1',
            'confirm_password': 'password2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password does not match')


    def test_register_existing_username(self):
        """Test registration with an existing username"""
        User.objects.create_user(username='testuser', email='test@example.com', password='password')
        response = self.client.post(reverse('register'), {
            'fname': 'Test',
            'lname': 'User',
            'username': 'testuser',  # Duplicate username
            'email': 'newuser@example.com',
            'password': 'password',
            'confirm_password': 'password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username already exists')
        

class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login_success(self):
        """Test successful login"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 302)


class LogoutViewTest(TestCase):
    def test_logout(self):
        """Test logout"""
        self.client.force_login(User.objects.create_user(username='testuser', password='password'))
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
    

