from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import Booking
from rooms.models import Room
from .serializers import CheckMyBookingSerializer, ManageBookingsSerializer


class GetMyBookings(APIView):
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = CheckMyBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)


class ManageBookings(APIView):
    def get(self, request):
        rooms = Room.objects.filter(owner=request.user)
        bookings = rooms[0].bookings.all()
        for i in range(1, len(rooms)):
            bookings |= rooms[i].bookings.all()
        serializer = ManageBookingsSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)


class CancelMyBooking(APIView):
    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        booking = self.get_object(pk)
        data = {"not_canceled": False}
        serializer = CheckMyBookingSerializer(
            booking,
            data=data,
            partial=True,
        )
        if serializer.is_valid():
            canceled_booking = serializer.save()
            serializer = CheckMyBookingSerializer(canceled_booking)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
