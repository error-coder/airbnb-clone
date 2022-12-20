from django.utils import timezone
from rest_framework import serializers
from .models import Booking

class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        # 유저에게 받고 싶은 데이터
        fields = ("check_in", "check_out", "guests",)

    # check_in과 check_out이 미래 날짜인지 확인
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check in should be smaller than check out.")
        if Booking.objects.filter(check_in__lte=data['check_in'], check_out__gte=data['check_out'],).exists():
        # check in과 check out 사이의 예약을 확인할 순 있는데 check_in, out 이후에 존재하는 booking을 확인 못함
        # Booking.objects.filter(check_in__gte=data['check_in'], check_out__lte=data['check_out'],).exists()
            raise serializers.ValidationError("Those (or some) of those dates are already taken.")
        return data

class CreateExperienceBookingSerializer(serializers.ModelSerializer):

    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = ("experience_time", "guests",)


    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")

        return value


class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "experience_time", "guests",)