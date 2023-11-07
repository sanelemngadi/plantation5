from django.urls import path
from inventory import views

urlpatterns = [
    path("", views.inventory_view, name="inventory"),
    path("remove/<int:pk>/", views.stock_remove_view, name="stock-remove"),
    path("update/<int:pk>/", views.stock_update_view, name="stock-update"),
]