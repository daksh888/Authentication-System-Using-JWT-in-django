from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser



class AuthTests(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')  
        self.login_url = reverse('login')       
        self.valid_payload = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }
        self.invalid_payload = {
            'username': '',  # Missing username
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }
    
    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')

    def test_register_user_failure(self):
        response = self.client.post(self.register_url, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_login_user_success(self):
        # First, register the user
        self.client.post(self.register_url, self.valid_payload)
        
        # Now, try to login
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Assuming the token is returned in the response

    def test_login_user_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

