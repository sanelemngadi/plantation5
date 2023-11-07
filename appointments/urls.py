from django.urls import path
from appointments import views

urlpatterns = [
    path("", views.appointment_list_view, name="appointments"),
    path("create-new/", views.appointment_create_view, name="new-appointment"),
    path("confirm-appointment/<int:pk>/", views.appointment_confirm_view, name="confirm-appointment"),
    path("appointment/<int:pk>/", views.appointment_detail_view, name="detail-appointment"),
]