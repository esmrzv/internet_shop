from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegisterView, user_verify, restore_password

app_name = UsersConfig.name
urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', user_verify, name='email-confirm'),
    path('password_restore/', restore_password, name='password-restore'),
]
