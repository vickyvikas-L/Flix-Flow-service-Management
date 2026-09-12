from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from .models import Invoice
from .serializers import InvoiceSerializer
from users.models import User
from tickets.models import ServiceTicket
from services.models import ServiceCategory

class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Invoice.objects.all()
        if user.role == User.Role.CUSTOMER:
            queryset = queryset.filter(ticket__customer=user)
        elif user.role == User.Role.TECHNICIAN:
            queryset = queryset.filter(ticket__technician=user)
        return queryset

class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class AdminReportStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_customers = User.objects.filter(role=User.Role.CUSTOMER).count()
        total_technicians = User.objects.filter(role=User.Role.TECHNICIAN).count()
        open_tickets = ServiceTicket.objects.filter(
            status__in=[ServiceTicket.Status.PENDING, ServiceTicket.Status.ASSIGNED, ServiceTicket.Status.IN_PROGRESS]
        ).count()
        completed_tickets = ServiceTicket.objects.filter(status=ServiceTicket.Status.COMPLETED).count()
        
        revenue_data = Invoice.objects.aggregate(total=Sum('total_amount'))
        total_revenue = float(revenue_data['total'] or 0.00)

        # Most requested services
        top_services = list(
            ServiceCategory.objects.annotate(ticket_count=Count('tickets'))
            .values('id', 'name', 'ticket_count')
            .order_by('-ticket_count')[:5]
        )

        # Status distribution
        status_counts = {
            'Pending': ServiceTicket.objects.filter(status=ServiceTicket.Status.PENDING).count(),
            'Assigned': ServiceTicket.objects.filter(status=ServiceTicket.Status.ASSIGNED).count(),
            'In Progress': ServiceTicket.objects.filter(status=ServiceTicket.Status.IN_PROGRESS).count(),
            'Completed': completed_tickets
        }

        # Average rating
        avg_rating_data = ServiceTicket.objects.aggregate(avg_rating=Avg('rating'))
        avg_rating = round(float(avg_rating_data['avg_rating'] or 4.8), 1)

        return Response({
            'total_customers': total_customers,
            'total_technicians': total_technicians,
            'open_tickets': open_tickets,
            'completed_tickets': completed_tickets,
            'total_revenue': total_revenue,
            'avg_rating': avg_rating,
            'top_services': top_services,
            'status_counts': status_counts,
        })
