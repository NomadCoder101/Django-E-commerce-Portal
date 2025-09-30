from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('deals/', views.deals, name='deals'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('discount/apply/', views.apply_discount, name='apply_discount'),
    path('discount/remove/', views.remove_discount, name='remove_discount'),
]