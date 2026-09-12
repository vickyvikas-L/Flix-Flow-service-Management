from django.urls import path
from .views import NotificationListView, MarkNotificationsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('read-all/', MarkNotificationsReadView.as_view(), name='notification_read_all'),
]
