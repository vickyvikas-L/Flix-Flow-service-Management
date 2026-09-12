from rest_framework import serializers
from .models import ServiceTicket
from users.serializers import UserSerializer
from services.serializers import ServiceCategorySerializer

class ServiceTicketSerializer(serializers.ModelSerializer):
    customer_details = UserSerializer(source='customer', read_only=True)
    technician_details = UserSerializer(source='technician', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    invoice_details = serializers.SerializerMethodField()

    class Meta:
        model = ServiceTicket
        fields = [
            'id', 'ticket_number', 'customer', 'customer_details',
            'category', 'category_name', 'category_icon',
            'title', 'description', 'priority', 'status',
            'image', 'technician', 'technician_details',
            'technician_notes', 'rating', 'review_text',
            'created_at', 'updated_at', 'completed_at',
            'invoice_details'
        ]
        read_only_fields = ['id', 'ticket_number', 'customer', 'created_at', 'updated_at', 'completed_at']

    def get_invoice_details(self, obj):
        if hasattr(obj, 'invoice'):
            inv = obj.invoice
            return {
                'id': inv.id,
                'invoice_number': inv.invoice_number,
                'service_charge': float(inv.service_charge),
                'additional_charge': float(inv.additional_charge),
                'tax_amount': float(inv.tax_amount),
                'total_amount': float(inv.total_amount),
                'payment_status': inv.payment_status,
                'issued_at': inv.issued_at
            }
        return None
