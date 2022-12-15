from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomListSerializer
from .models import Wishlist

class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(many=True, read_only=True,)

    class Meta:
        model = Wishlist
        # 유저에게 위시리스트의 이름과 안에 있는 방을 보여줌(유저는 표시X) -> 위시리스트를 보고 있는 유저가 위시리스트의 소유자이기 때문
        fields = ("pk", "name", "rooms",)