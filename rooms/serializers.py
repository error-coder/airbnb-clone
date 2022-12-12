from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description",)


class RoomDetailSerializer(ModelSerializer):

    # owner를 가져올 때 TinyUserSerializer를 사용하라고 알려줌, read_only -> 우리가 방을 생성할 때 serializer는 owner에 대한 정보를 요구하지 않음
    owner = TinyUserSerializer(read_only=True) 
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True) # array가 아니고 숫자 하나면 many=True를 사용X

    class Meta:
        model = Room
        fields = "__all__"

class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "country", "city", "price",)
