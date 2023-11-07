from django.urls import path
from rentals import views

urlpatterns = [
    path("", views.rental_list_view, name="rentals"),
    path("create-new-rental/product/<int:pk>/", views.rental_create_view, name="new-rental"),
    path("confirm-rental/<int:pk>/", views.confirm_rental_view, name="confirm-rental"),
    path("item/<int:pk>/", views.rental_detail_view, name="rental-detail"),
    path("rental-success/<int:pk>/", views.rental_success, name="rental-success"),
    path("rental-verify/<int:pk>/", views.verify_rental_identity_view, name="rental-verify"),
    path("rental-reject/<int:pk>/", views.reject_rental_identity_files, name="rental-reject"),
    path("rental-collect/<int:pk>/", views.rental_collection_view, name="rental-collected"),
    path("rental-return/<int:pk>/", views.rental_returned_view, name="rental-returned"),
]