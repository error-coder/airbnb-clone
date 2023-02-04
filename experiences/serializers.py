from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer
from .models import Perk, Experience
from rest_framework.serializers import ModelSerializer


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    perks = PerkSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = "__all__"
