from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from .models import ServiceTicket
from .serializers import ServiceTicketSerializer
from users.models import User
from payments.models import Invoice
from notifications.models import Notification

class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ServiceTicket.objects.all()

        # Role restriction
        if user.role == User.Role.CUSTOMER:
            queryset = queryset.filter(customer=user)
        elif user.role == User.Role.TECHNICIAN:
            queryset = queryset.filter(technician=user)

        # Search parameter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(ticket_number__icontains=search) |
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(customer__username__icontains=search) |
                Q(category__name__icontains=search)
            )

        # Status filter
        status_param = self.request.query_params.get('status', None)
        if status_param:
            statuses = status_param.split(',')
            queryset = queryset.filter(status__in=statuses)

        # Priority filter
        priority_param = self.request.query_params.get('priority', None)
        if priority_param:
            priorities = priority_param.split(',')
            queryset = queryset.filter(priority__in=priorities)

        return queryset

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceTicket.objects.all()
    serializer_class = ServiceTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

class AssignTechnicianView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.role != User.Role.ADMIN:
            return Response({'detail': 'Only admins can assign technicians'}, status=status.HTTP_403_FORBIDDEN)

        try:
            ticket = ServiceTicket.objects.get(pk=pk)
        except ServiceTicket.DoesNotExist:
            return Response({'detail': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        technician_id = request.data.get('technician_id')
        try:
            technician = User.objects.get(id=technician_id, role=User.Role.TECHNICIAN)
        except User.DoesNotExist:
            return Response({'detail': 'Valid technician not found'}, status=status.HTTP_400_BAD_REQUEST)

        ticket.technician = technician
        if ticket.status == ServiceTicket.Status.PENDING:
            ticket.status = ServiceTicket.Status.ASSIGNED
        ticket.save()

        # Send notification to technician
        Notification.objects.create(
            user=technician,
            ticket=ticket,
            title="New Service Request Assigned",
            message=f"🔔 Service request {ticket.ticket_number} ({ticket.title}) has been assigned to you."
        )

        return Response(ServiceTicketSerializer(ticket).data)

class UpdateTicketStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            ticket = ServiceTicket.objects.get(pk=pk)
        except ServiceTicket.DoesNotExist:
            return Response({'detail': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        technician_notes = request.data.get('technician_notes', '')

        if new_status not in [choice[0] for choice in ServiceTicket.Status.choices]:
            return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = new_status
        if technician_notes:
            ticket.technician_notes = technician_notes

        if new_status == ServiceTicket.Status.COMPLETED:
            ticket.completed_at = timezone.now()
            
            # Auto-generate Invoice if not exists
            if not hasattr(ticket, 'invoice'):
                base_fee = float(ticket.category.base_price) if ticket.category else 1500.00
                service_charge = float(request.data.get('service_charge', base_fee))
                additional_charge = float(request.data.get('additional_charge', 300.00))
                
                Invoice.objects.create(
                    ticket=ticket,
                    service_charge=service_charge,
                    additional_charge=additional_charge,
                    payment_status=Invoice.PaymentStatus.PAID
                )

            # Send Notification to Customer
            Notification.objects.create(
                user=ticket.customer,
                ticket=ticket,
                title="Service Request Completed",
                message=f"🔔 Your service request {ticket.ticket_number} has been completed! Invoice generated."
            )

        ticket.save()
        return Response(ServiceTicketSerializer(ticket).data)

class RateTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            ticket = ServiceTicket.objects.get(pk=pk)
        except ServiceTicket.DoesNotExist:
            return Response({'detail': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        if ticket.customer != request.user:
            return Response({'detail': 'You can only rate your own tickets'}, status=status.HTTP_403_FORBIDDEN)

        rating = request.data.get('rating')
        review_text = request.data.get('review_text', '')

        if not rating or not (1 <= int(rating) <= 5):
            return Response({'detail': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)

        ticket.rating = int(rating)
        ticket.review_text = review_text
        ticket.save()

        return Response(ServiceTicketSerializer(ticket).data)
