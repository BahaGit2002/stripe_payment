from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('buy/<int:id>/', views.buy_item, name='buy_item'),
    path('order/<int:id>/', views.buy_order, name='buy_order'),
    path('payment-intent/<int:id>/', views.create_payment_intent, name='payment_intent'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
