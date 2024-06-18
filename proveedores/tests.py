from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Product

class UserProfileUpdateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_update_profile(self):
        url = reverse('proveedores:user_update')
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'password': '',
            'password2': '',
        }
        response = self.client.post(url, data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proveedores:profile'))
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_update_password(self):
        url = reverse('proveedores:user_update')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.post(url, data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proveedores:profile'))
        self.assertTrue(self.user.check_password('newpassword123'))

class ProductTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(user=self.user, name='Test Product', price=100.00, description='Test Description')

    def test_create_product(self):
        url = reverse('proveedores:product_new')
        data = {
            'name': 'New Product',
            'price': '50.00',
            'description': 'New Description',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proveedores:product_list'))
        self.assertEqual(Product.objects.count(), 2)
        new_product = Product.objects.get(name='New Product')
        self.assertEqual(new_product.price, 50.00)
        self.assertEqual(new_product.description, 'New Description')

    def test_update_product(self):
        url = reverse('proveedores:product_update', args=[self.product.id])
        data = {
            'name': 'Updated Product',
            'price': '150.00',
            'description': 'Updated Description',
        }
        response = self.client.post(url, data)
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proveedores:product_detail', args=[self.product.id]))
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.price, 150.00)
        self.assertEqual(self.product.description, 'Updated Description')

    def test_delete_product(self):
        url = reverse('proveedores:product_delete', args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proveedores:product_list'))
        self.assertEqual(Product.objects.count(), 0)