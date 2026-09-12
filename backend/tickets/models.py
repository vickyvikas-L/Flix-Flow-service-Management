from django.db import models
from django.conf import settings

class ServiceTicket(models.Model):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ASSIGNED = 'ASSIGNED', 'Assigned'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    ticket_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_tickets'
    )
    category = models.ForeignKey(
        'services.ServiceCategory',
        on_delete=models.PROTECT,
        related_name='tickets'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    image = models.ImageField(upload_to='ticket_images/', blank=True, null=True)
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )
    technician_notes = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    review_text = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            last_ticket = ServiceTicket.objects.order_by('-id').first()
            last_id = last_ticket.id if last_ticket else 1023
            self.ticket_number = f"#{last_id + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_number} - {self.title} ({self.status})"
