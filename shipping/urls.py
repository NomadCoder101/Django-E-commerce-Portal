from django.urls import path
from . import views

app_name = 'shipping'

urlpatterns = [
    path('addresses/', views.shipping_address_list, name='address_list'),
    path('addresses/add/', views.shipping_address_add, name='address_add'),
    path('addresses/<int:pk>/edit/', views.shipping_address_edit, name='address_edit'),
    path('addresses/<int:pk>/delete/', views.shipping_address_delete, name='address_delete'),
    path('addresses/<int:pk>/set-default/', views.set_default_address, name='set_default_address'),
    path('select-method/', views.select_shipping_method, name='select_method'),
]