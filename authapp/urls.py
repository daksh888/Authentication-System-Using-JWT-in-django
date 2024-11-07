from django.urls import path

from .views import  UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView,register_view,login_view,home_view,activate

urlpatterns = [
    path('', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]