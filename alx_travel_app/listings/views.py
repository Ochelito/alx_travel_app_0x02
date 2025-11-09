from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
import requests
import uuid

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on Listings
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on Bookings
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# -------------------------------
# ✅ CHAPA PAYMENT INTEGRATION
# -------------------------------

class InitiatePaymentView(APIView):
    """
    Initiate a payment with Chapa API.
    Creates a Payment object and returns the checkout URL.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        booking_id = request.data.get("booking_id")

        # Step 1: Validate booking
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Prevent duplicate payment
        if hasattr(booking, "payment"):
            return Response({"error": "Payment already exists for this booking."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Generate a unique reference
        tx_ref = str(uuid.uuid4())

        # Step 4: Calculate total amount (for now, assume 1 night = price_per_night)
        amount = booking.listing.price_per_night

        # Step 5: Prepare Chapa API request
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": str(amount),
            "currency": "NGN",  # Change to your currency if needed
            "email": booking.guest.email,
            "first_name": booking.guest.first_name or "User",
            "last_name": booking.guest.last_name or "Guest",
            "tx_ref": tx_ref,
            "callback_url": "http://localhost:8000/api/payments/verify/",  # Update for production
            "return_url": "http://localhost:8000/payment-success/",
            "customization": {
                "title": "AvenMile Booking Payment",
                "description": f"Payment for booking ID {booking.id}"
            }
        }

        response = requests.post(
            "https://api.chapa.co/v1/transaction/initialize",
            json=payload,
            headers=headers
        )

        result = response.json()

        # Step 6: Store Payment data
        if response.status_code == 200 and result.get("status") == "success":
            checkout_url = result["data"]["checkout_url"]

            Payment.objects.create(
                booking=booking,
                amount=amount,
                status="Pending",
                reference=tx_ref,
                transaction_id=result["data"]["id"]
            )

            return Response({
                "message": "Payment initiated successfully.",
                "checkout_url": checkout_url,
                "tx_ref": tx_ref
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Payment initiation failed.",
                "details": result
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentView(APIView):
    """
    Verify a payment from Chapa.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        tx_ref = request.query_params.get("tx_ref")

        if not tx_ref:
            return Response({"error": "tx_ref is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Retrieve payment
        try:
            payment = Payment.objects.get(reference=tx_ref)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Verify via Chapa API
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"

        response = requests.get(verify_url, headers=headers)
        result = response.json()

        # Step 3: Update payment status
        if result.get("status") == "success" and result["data"]["status"] == "success":
            payment.status = "Completed"
            payment.save()
            return Response({"message": "Payment verified successfully", "status": "Completed"})
        else:
            payment.status = "Failed"
            payment.save()
            return Response({"message": "Payment verification failed", "status": "Failed"})
