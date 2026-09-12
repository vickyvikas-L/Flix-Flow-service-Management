from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    ticket_number = serializers.CharField(source='ticket.ticket_number', read_only=True)
    customer_name = serializers.CharField(source='ticket.customer.get_full_name', read_only=True)
    customer_email = serializers.CharField(source='ticket.customer.email', read_only=True)
    category_name = serializers.CharField(source='ticket.category.name', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'ticket', 'ticket_number',
            'customer_name', 'customer_email', 'category_name',
            'service_charge', 'additional_charge', 'tax_amount',
            'total_amount', 'payment_status', 'issued_at', 'paid_at'
        ]
