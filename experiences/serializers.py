from rest_framework import serializers
from .models import Perk, Experience
from common.serializers import TinyUserSerializer
from medias.serializers import PhotoSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from wishlists.models import Wishlist


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "name",
            "details",
            "explanation",
        )


class ExperienceListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, experience):
        return experience.rating()

    def get_is_owner(self, experience):
        request = self.context.get("request")
        if request:
            return experience.host == request.user
        return False


class ExperienceDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    perks = PerkSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    reviews = ReviewSerializer(
        many=True,
        read_only=True,
    )
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = "__all__"

    def get_rating(self, experience):
        return experience.rating()

    def get_is_owner(self, experience):
        request = self.context.get("request")
        if request:
            return experience.host == request.user
        return False

    def get_is_liked(self, room):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    rooms__pk=room.pk,
                ).exists()

        return False