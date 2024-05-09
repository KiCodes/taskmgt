from . import views
from django.urls import path

urlpatterns = [
    path('signup', views.SignUpView.as_view(),name='signup'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('password_change', views.ChangePasswordView.as_view(), name='password_change'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]