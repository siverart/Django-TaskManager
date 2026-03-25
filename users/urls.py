from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path("register/", views.register, name="register"),
    path("register/thankyou", views.register_thankyou, name="register_thankyou"),
    path("activate/<str:uidb64>/<str:token>", views.activate, name="activate")
]