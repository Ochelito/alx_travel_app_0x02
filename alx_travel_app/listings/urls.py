from django.urls import path, include
from rest_framework import routers
from .views import ListingViewSet, BookingViewSet, InitiatePaymentView, VerifyPaymentView   


router = routers.DefaultRouter()
# register your viewsets here e.g. router.register(r'properties', views.PropertyViewSet)
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payments/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]
