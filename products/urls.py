from django.urls import path
from products import views

urlpatterns = [
    path("", views.product_list_view, name="product-list"),
    path("product/<int:pk>/", views.product_detail_view, name="product-detail"),
    path("product-remove/<int:pk>/", views.product_remove_view, name="product-remove"),
    path("product-update/<int:pk>/", views.product_update_view, name="product-update"),
    path("product-create/", views.product_create_view, name="product-create"),
]