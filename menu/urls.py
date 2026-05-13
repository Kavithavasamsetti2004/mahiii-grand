from django.urls import path
from . import views

urlpatterns = [
    path('',             views.welcome,      name='welcome'),
    path('menu/',        views.menu_page,    name='menu_page'),
    path('place-order/', views.place_order,  name='place_order'),
    path('payment/',     views.payment_page, name='payment_page'),
    path('mark-paid/<int:order_id>/', views.mark_paid, name='mark_paid'),
]