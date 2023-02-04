from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer
from .models import Perk, Experience
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


