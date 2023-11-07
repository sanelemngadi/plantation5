from django.urls import path
from warehouse import views

urlpatterns = [
    path("", views.warehouse_view, name="warehouse")
]