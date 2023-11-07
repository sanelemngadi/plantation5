from django.urls import path
from user import views 

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("register-supplier/", views.supplier_register_view, name="supplier-register"),
    path("logout/", views.logout_view, name="logout"),
    path("settings/", views.settings_view, name="settings"),
    path("manage-users/", views.manage_users_view, name="manage-users"),
    path("update/<int:pk>/", views.user_update_view, name="user-update"),
    path("remove/<int:pk>/", views.user_remove_view, name="user-remove"),
]