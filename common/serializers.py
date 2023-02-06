from rest_framework.serializers import ModelSerializer
from users.models import User
from rooms.models import Room


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class TinyRoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
        )

