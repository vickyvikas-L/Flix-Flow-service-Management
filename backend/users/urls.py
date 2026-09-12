from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, UserProfileView, TechnicianListView, AllUsersListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserProfileView.as_view(), name='auth_me'),
    path('technicians/', TechnicianListView.as_view(), name='technician_list'),
    path('users/', AllUsersListView.as_view(), name='all_users_list'),
]
