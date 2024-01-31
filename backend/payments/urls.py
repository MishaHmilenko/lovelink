from django.urls import path

from payments import views

app_name = 'payments'

urlpatterns = [
    path('config/', views.StripeConfigAPIView.as_view(), name='config'),
    path('products/', views.GetAllProductsAPIView.as_view(), name='products'),
    path('create-checkout-session/', views.CreateCheckOutSession.as_view(), name='create-checkout-session'),
    path('webhook/', views.StripeWebHookAPIView.as_view(), name='webhook'),
]
