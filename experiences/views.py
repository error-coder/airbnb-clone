from django.db import transaction
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from categories.models import Category
from bookings.models import Booking
from bookings.serializers import CreateExperienceBookingSerializer, PublicBookingSerializer
from .models import Perk, Experience
from . import serializers


class Experiences(APIView):
    def get(self, request):
        experiences = Experience.objects.all()
        serializer = serializers.ExperienceSerializer(experiences, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceSerializer(data=request.data)

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")

            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be experience")
            except Category.DoesNotExist:
                raise ParseError(detail="Category not found")

            try:
                with transaction.atomic():
                    experience = serializer.save(host=request.user, category=category)

                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)

                    return Response(serializers.ExperienceSerializer(experience).data)

            except Exception:
                raise ParseError("perk not found")
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        return Response(serializers.ExperienceSerializer(experience).data)

    def put(self, request, pk):
        experience = self.get_object(pk)

        if experience.host != request.user:
            raise PermissionDenied

        serializer = serializers.ExperienceSerializer(experience, data=request.data, partial=True)

        if serializer.is_valid():
            category_pk = request.data.get("category")

            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("The category kind should be experience")
                except Category.DoesNotExist:
                    raise ParseError(detail="Category not found")

            try:
                with transaction.atomic():
                    if category_pk:
                        experience = serializer.save(category=category)
                    else:
                        experience = serializer.save()

                    perks = request.data.get("perks")
                    if perks:
                        experience.perks.clear()
                        for perk_pk in perks:
                            perk = Perk.objects.get(pk=perk_pk)
                            experience.perks.add(perk)

                    return Response(serializers.ExperienceSerializer(experience).data)

            except Exception:
                raise ParseError("perk not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)

        if experience.host != request.user:
            raise PermissionDenied

        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            experience.perks.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class ExperienceBookings(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gt=now,
        )[start:end]
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound

    def get(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)

        return Response(PublicBookingSerializer(booking).data)

    def put(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)

        if booking.user.pk != request.user.pk:
            raise PermissionDenied

        serializer = CreateExperienceBookingSerializer(booking, data=request.data, partial=True)

        if serializer.is_valid():
            booking = serializer.save()
            serializer = PublicBookingSerializer(booking)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):

        booking = self.get_booking(booking_pk)

        if booking.user.pk != request.user.pk:
            raise PermissionDenied

        booking.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class Perks(APIView):
    def get(self, request):
        perks = Perk.objects.all()
        serializer = serializers.PerkSerializer(perks, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)

        if serializer.is_valid():
            perk = serializer.save()
            return Response(serializers.PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)

    def get(self, request, pk):
        perk = self.get_object(pk)
        return Response(serializers.PerkSerializer(perk).data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk, data=request.data, partial=True)

        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        return Response(serializers.PerkSerializer(perk).data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk, data=request.data, partial=True)

        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
