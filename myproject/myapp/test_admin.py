from django.test import TestCase
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from myapp.admin import RegisterAdmin
from myapp.models import Register

class RegisterAdminTests(TestCase):

    def setUp(self):
        # Create a user to simulate an admin
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.admin = RegisterAdmin(model=Register, admin_site=site)

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(None))

    def test_has_change_permission(self):
        self.assertFalse(self.admin.has_change_permission(None))

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(None))

    def test_readonly_fields(self):
        expected_readonly_fields = [field.name for field in Register._meta.fields]
        self.assertEqual(self.admin.readonly_fields, expected_readonly_fields)
