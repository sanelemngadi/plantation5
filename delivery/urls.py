from django.urls import path
from delivery import views

urlpatterns = [
    path("", views.delivery_list_view, name="delivery-list")
]