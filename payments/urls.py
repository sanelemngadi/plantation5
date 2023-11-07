from django.urls import path
from payments import views

urlpatterns = [
    path("", views.payment_view, name="payment"),
    path("success/", views.payment_successful_view, name="successful"),
    path("cancelled/", views.payment_cancelled_view, name="cancelled"),
]