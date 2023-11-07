from django.urls import path
from notifications import views

urlpatterns = [
    path("", views.notification_list_view, name="notifications"),
    path("notification/<int:pk>/", views.notification_detail_view, name="notification-detail"),
    path("notification-order/<int:pk>/", views.notification_order_view, name="notification-order"),
    path("pay-order/<int:pk>/", views.pay_order_view, name="pay-order"),
]
