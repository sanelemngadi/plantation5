from django.urls import path
from events import views

urlpatterns = [
    path("", views.event_list_view, name="events"),
    path("create-new/", views.event_create_view, name="new-event"),
    path("event/<int:pk>/", views.event_detail_view, name="event"),
    # path("download/<int:pk>/", views.download_event_qr_view, name="download_pq"),
    path("download_qr/<int:event_id>/", views.event_payment_success, name="download"),
]