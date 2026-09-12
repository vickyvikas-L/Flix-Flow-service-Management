from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, AdminReportStatsView

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('reports/stats/', AdminReportStatsView.as_view(), name='admin_reports_stats'),
]
