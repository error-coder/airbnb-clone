from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from common.views import get_object, check_owner, get_page
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicRoomBookingSerializer, CreateRoomBookingSerializer


def check_Category(category_pk):
    try:
        category = Category.objects.get(pk=category_pk)
        if category.kind == Category.CategoryKindChoices.EXPERIENCES:
            raise ParseError("The category kind should be 'rooms'")
        return category

    except Category.DoesNotExist:
        raise ParseError("Category not found")


def add_amenities(amenities, room):
    for amenity_pk in amenities:
        amenity = Amenity.objects.get(pk=amenity_pk)
        room.amenities.add(amenity)


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)

        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):
    def get(self, request, pk):
        amenity = get_object(Amenity, pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = get_object(Amenity, pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        amenity = get_object(Amenity, pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all().order_by("-pk")
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                category = check_Category(category_pk)
            else:
                raise ParseError("Category is required.")

            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )

                    amenities = request.data.get("amenities")

                    if amenities:
                        add_amenities(amenities, room)

                    serializer = RoomDetailSerializer(
                        room,
                        context={"request": request},
                    )
                    return Response(serializer.data)

            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomDetial(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        room = get_object(Room, pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):

        room = get_object(Room, pk)

        check_owner(request, room.owner)

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            category_pk = request.data.get("category")

            if category_pk:
                category = check_Category(request)

            try:
                with transaction.atomic():
                    if category_pk:
                        room = serializer.save(category=category)
                    else:
                        room = serializer.save()

                    amenities = request.data.get("amenities")

                    if amenities != None:
                        room.amenities.clear()

                        if amenities:
                            add_amenities(amenities, room)

                    serializer = RoomDetailSerializer(
                        room,
                        context={"request": request},
                    )
                    return Response(serializer.data)

            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = get_object(Room, pk)

        check_owner(request, room.owner)

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        page = get_page(request)
        page_size = settings.PAGE_SIZE

        room = get_object(Room, pk)
        paginator = Paginator(
            room.reviews.all(),
            per_page=page_size,
            orphans=2,
        )
        serializer = ReviewSerializer(
            paginator.get_page(page),
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=get_object(Room, pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomAmenities(APIView):
    def get(self, request, pk):
        page = get_page(request)
        page_size = settings.PAGE_SIZE

        room = get_object(Room, pk)
        paginator = Paginator(
            room.amenities.all(),
            per_page=page_size,
            orphans=2,
        )
        serializer = ReviewSerializer(paginator.get_page(page), many=True)
        return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        room = get_object(Room, pk)

        check_owner(request, room.owner)

        serializer = PhotoSerializer(data=request.data)

        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        room = get_object(Room, pk)
        now = timezone.localtime(timezone.now()).date()

        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gte=now,
        )
        serializer = PublicRoomBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = get_object(Room, pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data,
            context={"room": room},
        )

        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = CreateRoomBookingSerializer(booking)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class RoomBookingCheck(APIView):
    def get(self, request, pk):
        room = get_object(Room, pk)
        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")

        exists = Booking.objects.filter(
            room=room,
            check_in__lte=check_out,
            check_out__gte=check_in,
        ).exists()

        return Response({"ok": not exists})


class RoomBookingDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk, booking_pk):
        booking = get_object(Booking, booking_pk)
        serializer = PublicRoomBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk, booking_pk):
        booking = get_object(Booking, booking_pk)
        room = get_object(Room, pk)

        check_owner(request, booking.user)

        serializer = CreateRoomBookingSerializer(
            booking,
            data=request.data,
            partial=True,
            context={"room": room},
        )

        if serializer.is_valid():
            updated_booking = serializer.save()
            serializer = PublicRoomBookingSerializer(updated_booking)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):
        booking = get_object(Booking, booking_pk)
        check_owner(request, booking.user)
        booking.delete()
        return Response(status=HTTP_204_NO_CONTENT)
