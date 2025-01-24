from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('manufacturer', 'Manufacturer or Product Seller'),
        ('machine_vendor', 'Machine Vendor'),
        ('professional_worker', 'Professional Worker'),
    ]
    user_type = models.CharField(max_length=30, choices=USER_TYPES)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="customuser",
    )

class ManufacturerOrProductSeller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, blank=True)
    unique_vendor_id = models.CharField(max_length=10, unique=True, blank=True)
    company_name = models.CharField(max_length=255)
    gst_certificate = models.FileField(upload_to='documents/', blank=True)
    pan_card_company = models.FileField(upload_to='documents/', blank=True)
    pan_card_owner = models.FileField(upload_to='documents/', blank=True)
    aadhar_card = models.FileField(upload_to='documents/', blank=True)
    bank_details = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)

class MachineVendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, blank=True)
    unique_vendor_id = models.CharField(max_length=10, unique=True, blank=True)
    aadhar_card = models.FileField(upload_to='documents/', blank=True)
    pan_card = models.FileField(upload_to='documents/', blank=True)
    gst_details = models.TextField(blank=True)
    bank_details = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)


class ProfessionalWorker(models.Model):
    CATEGORY_CHOICES = [
        ('architect', 'Architect'),
        ('interior_designer', 'Interior Designer'),
        ('civil_engineer', 'Civil Engineer'),
        ('painter', 'Painter'),
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('contractor', 'Contractor'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, blank=True)
    unique_vendor_id = models.CharField(max_length=10, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    aadhar_card = models.FileField(upload_to='documents/', blank=True)
    pan_card = models.FileField(upload_to='documents/', blank=True)
    gst_details = models.TextField(blank=True)
    bank_details = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)