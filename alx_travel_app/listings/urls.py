from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
# register your viewsets here e.g. router.register(r'properties', views.PropertyViewSet)
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
path('', include(router.urls)),
]
