from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('verify/<str:uidb64>/', views.CodeVerifyView.as_view(), name='code'),
    path('forgot/password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('forgot/password/done/', views.ForgotPasswordDoneView.as_view(), name='forgot_done'),
    path('reset/password/<str:uidb64>/<str:token>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('reset/password/done/', views.ResetPasswordDoneView.as_view(), name='reset_done'),

]
