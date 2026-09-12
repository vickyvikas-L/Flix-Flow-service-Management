from django.db import models

class Invoice(models.Model):
    class PaymentStatus(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PAID = 'PAID', 'Paid'

    ticket = models.OneToOneField(
        'tickets.ServiceTicket',
        on_delete=models.CASCADE,
        related_name='invoice'
    )
    invoice_number = models.CharField(max_length=30, unique=True, editable=False)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    additional_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PAID
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{self.ticket.ticket_number.replace('#', '')}"
        self.total_amount = self.service_charge + self.additional_charge + self.tax_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - Total ₹{self.total_amount} ({self.payment_status})"
