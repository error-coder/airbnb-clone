from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers
from .models import Perk, Experience
from common.views import get_object, get_page, check_owner
from bookings.models import Booking
from bookings.serializers import (
    PublicExperienceBookingSerializer,
    CreateExperienceBookingSerializer,
    PublicExperienceBookingSerializer,
)
from categories.models import Category


def check_Category(category_pk):
    try:
        category = Category.objects.get(pk=category_pk)
        if category.kind == Category.CategoryKindChoices.ROOMS:
            raise ParseError("The category kind should be 'experiences'")
        return category

    except Category.DoesNotExist:
        raise ParseError("Category not found")


def add_perks(perks, experience):
    for perk_pk in perks:
        perk = Perk.objects.get(pk=perk_pk)
        experience.perks.add(perk)


class Experiences(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        page = get_page(request)
        page_size = settings.PAGE_SIZE

        paginator = Paginator(
            Experience.objects.all(),
            per_page=page_size,
            orphans=2,
        )
        serializer = serializers.ExperienceListSerializer(
            paginator.get_page(page),
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceDetailSerializer(data=request.data)

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                category = check_Category(category_pk)
            else:
                raise ParseError("Category is required.")

            try:
                with transaction.atomic():
                    if category_pk:
                        experience = serializer.save(
                            host=request.user,
                            category=category,
                        )
                    else:
                        experience = serializer.save()

                    perks = request.data.get("perks")

                    if perks:
                        add_perks(perks, experience)

                    serializer = serializers.ExperienceDetailSerializer(
                        experience,
                        context={"request": request},
                    )
                    return Response(serializer.data)

            except Exception:
                raise ParseError("Perk not found")
        else:
            return Response(serializer.errors)


class ExperiencesDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        experience = get_object(Experience, pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = get_object(Experience, pk)
        check_owner(request, experience.host)

        serializer = serializers.ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                category = check_Category(category_pk)

            try:
                with transaction.atomic():
                    if category_pk:
                        experience = serializer.save(category=category)
                    else:
                        experience = serializer.save()

                    perks = request.data.get("perks")

                    if perks != None:
                        experience.perks.clear()

                        if perks:
                            add_perks(perks, experience)

                    serializer = serializers.ExperienceDetailSerializer(
                        experience,
                        context={"request": request},
                    )
                    return Response(serializer.data)

            except Exception:
                raise ParseError("Amenity not found")

        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = get_object(Experience, pk)
        check_owner(request, experience.host)

        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        experience = get_object(Experience, pk)
        now = timezone.localtime(timezone.now())

        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gte=now,
        )
        serializer = PublicExperienceBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = get_object(Experience, pk)

        serializer = CreateExperienceBookingSerializer(
            data=request.data,
            context={"experience": experience},
        )

        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = CreateExperienceBookingSerializer(booking)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class ExperienceBookingDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk, booking_pk):
        booking = get_object(Booking, booking_pk)
        serializer = PublicExperienceBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk, booking_pk):
        booking = get_object(Booking, booking_pk)
        experience = get_object(Experience, pk)

        check_owner(request, booking.user)

        serializer = CreateExperienceBookingSerializer(
            booking,
            data=request.data,
            partial=True,
            context={"experience": experience},
        )

        if serializer.is_valid():
            updated_booking = serializer.save()
            serializer = PublicExperienceBookingSerializer(updated_booking)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):
        booking = get_object(Booking, booking_pk)
        check_owner(request, booking.user)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = serializers.PerkSerializer(
            all_perks,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)

        if serializer.is_valid():
            perk = serializer.save()
            return Response(serializers.PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get(self, request, pk):
        perk = get_object(Perk, pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = get_object(Perk, pk)
        serializer = serializers.PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            serializer = serializers.PerkSerializer(updated_perk)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)