from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('<int:order_id>/track/', views.order_track, name='track'),
    path('<int:order_id>/invoice/', views.order_invoice, name='invoice'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel'),
]