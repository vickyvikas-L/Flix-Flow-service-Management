from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    ticket_number = serializers.CharField(source='ticket.ticket_number', read_only=True, allow_null=True)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'ticket', 'ticket_number', 'created_at']
