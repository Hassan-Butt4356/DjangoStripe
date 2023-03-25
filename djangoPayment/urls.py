from django.contrib import admin
from django.urls import path
from checkout.views import (
    success,
    cancel,
    checkoutsessioncreate,
    checkoutsessioncreateProduct,
    stripe_webhook,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('success/', success,name='success'),
    path('create-checkout-session/', checkoutsessioncreate,name='create-checkout-session'),
    path('create-checkout-session/<str:pk>/<int:quantity>/', checkoutsessioncreateProduct,name='create-checkout-session-product'),
    path('cancel/', cancel,name='cancel'),
    path('stripe/webhook/', stripe_webhook,name='webhook'),
]
