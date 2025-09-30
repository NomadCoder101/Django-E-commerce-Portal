from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('addresses/', views.addresses, name='addresses'),
    path('orders/', views.orders, name='orders'),
]