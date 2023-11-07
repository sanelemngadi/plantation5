from django.urls import path
from cart import views

urlpatterns = [
    path("", views.cart_list_view, name="cart"),
    path("add-to-cart/<int:pk>/<str:path>/", views.add_to_cart_view, name="add-to-cart"),
    path("update-cart/product/<int:pk>/", views.update_cart_view, name="update-cart"),
    path("remove-cart-item/product/<int:pk>/", views.remove_from_cart_view, name="remove-cart-item"),
    path("checkout/", views.checkout_view, name="checkout"),
]
