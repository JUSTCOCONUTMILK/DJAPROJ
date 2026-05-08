from django.contrib.auth import views as auth_views
from django.urls import path
from .views import admin_panel_view, make_admin_view, register_view, toggle_ban_view

app_name = "users"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register_view, name="register"),
    path("admin-panel/", admin_panel_view, name="admin_panel"),
    path("ban/<int:user_id>/", toggle_ban_view, name="toggle_ban"),
    path("make-admin/<int:user_id>/", make_admin_view, name="make_admin"),
]
