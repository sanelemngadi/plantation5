from django.urls import path
from orders import views
# initiate_payment

urlpatterns = [
    path("", views.order_list_view, name="orders"),
    path("item-invoice/order/<int:pk>/", views.page_invoice_view, name="item-invoice"),
    path("pay-for-order/<int:order>/", views.pay_for_order_view, name="pay-for-order"),
    path("pay-order-success/<int:order_id>/", views.order_paid_success_view, name="pay-order-success"),
]