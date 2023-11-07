from django.urls import path
from suppliers import views

urlpatterns = [
    path("", views.supplier_list_view, name="suppliers"),
    # path("create/", views.supplier_create_view, name="supplier-create"),
    path("update/<int:pk>/", views.supplier_update_view, name="supplier-update"),
    path("remove/<int:pk>/", views.supplier_remove_view, name="supplier-remove"),
    path("detail-supplier/<int:pk>/", views.supplier_detail_view, name="supplier-detail"),
    path("supplier-order-accept/<int:pk>/", views.supplier_order_accept, name="supplier-order-accept"),
    path("del/<int:pk>/<int:sup>/", views.delete_order_item, name="del-sup-item"),
    path("confirm-order/<int:pk>/", views.confirm_order_to_supplier, name="confirm-order"),
    path("supplier-order-list/", views.supplier_order_list, name="supplier-order-list"),
    path("supplier-sent/<int:pk>/", views.send_order_to_supplier, name="supplier-order-sent"),
    path("supplier-invoice/<int:pk>/", views.supplier_order_invoice, name="supplier-order-invoice"),
    path("supplier-orders/", views.supplier_order_list_view, name="supplier-orders"),
]