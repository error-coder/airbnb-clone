from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Review
from common.serializers import TinyUserSerializer, TinyRoomSerializer


class ReviewSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )


class UserReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "payload",
            "rating",
            "created_at",
        )


class HostReviewSerializer(ModelSerializer):
    room = TinyRoomSerializer()

    class Meta:
        model = Review
        fields = (
            "room",
            "created_at",
            "payload",
            "rating",
        )