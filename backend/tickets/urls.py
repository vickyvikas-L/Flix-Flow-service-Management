from django.urls import path
from .views import (
    TicketListCreateView,
    TicketDetailView,
    AssignTechnicianView,
    UpdateTicketStatusView,
    RateTicketView
)

urlpatterns = [
    path('', TicketListCreateView.as_view(), name='ticket_list_create'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/assign/', AssignTechnicianView.as_view(), name='ticket_assign'),
    path('<int:pk>/status/', UpdateTicketStatusView.as_view(), name='ticket_status'),
    path('<int:pk>/rate/', RateTicketView.as_view(), name='ticket_rate'),
]
