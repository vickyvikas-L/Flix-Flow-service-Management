from django.urls import path
from .views import ServiceCategoryListCreateView, ServiceCategoryDetailView

urlpatterns = [
    path('', ServiceCategoryListCreateView.as_view(), name='services_list'),
    path('<int:pk>/', ServiceCategoryDetailView.as_view(), name='service_detail'),
]
