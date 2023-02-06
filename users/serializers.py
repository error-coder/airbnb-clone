from django.conf import settings
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User
from reviews.models import Review
from rooms.models import Room
from rooms.serializers import RoomListSerializer
from reviews.serializers import UserReviewSerializer, HostReviewSerializer


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )


class PublicUserSerializer(ModelSerializer):
    reviews = SerializerMethodField()
    host_reviews = SerializerMethodField()
    rooms = SerializerMethodField()
    class Meta:
        model = User
        exclude = (
            "id",
            "password",
            "is_superuser",
            "is_host",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )

    def get_reviews(self, user):
        recent_reviews = Review.objects.filter(user=user).order_by("-pk")[
            : settings.PAGE_SIZE
        ]
        return UserReviewSerializer(recent_reviews, many=True).data

    def get_host_reviews(self, user):
        reviews = Review.objects.filter(room__owner=user)[:10]
        return HostReviewSerializer(reviews, many=True).data

    def get_rooms(self, user):
        request = self.context.get("request")
        recent_rooms = Room.objects.filter(owner=user).order_by("-pk")[
            : settings.PAGE_SIZE
        ]

        return RoomListSerializer(
            recent_rooms,
            many=True,
            context={"request": request},
        ).data