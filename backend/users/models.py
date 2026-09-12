from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        TECHNICIAN = 'TECHNICIAN', 'Technician'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True, help_text="For technicians")
    is_available = models.BooleanField(default=True, help_text="Available for job assignment")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
