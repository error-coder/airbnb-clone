from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description",)


class RoomDetailSerializer(ModelSerializer):

    # owner를 가져올 때 TinyUserSerializer를 사용하라고 알려줌, read_only -> 우리가 방을 생성할 때 serializer는 owner에 대한 정보를 요구하지 않음
    owner = TinyUserSerializer(read_only=True) 
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True) # array가 아니고 숫자 하나면 many=True를 사용X
    rating = serializers.SerializerMethodField() # potato의 값을 계산할 method를 만들라고함
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room): # 이름앞에 무조건 get_을 붙여야 함
        print(self.context)
        return room.rating()

    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context['request']
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists() # 유저가 여러 개의 wishlist를 가질 수 있기 때문에 filter 사용

class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city", "price", "rating", "is_owner","photos",)

    def get_rating(self, room): 
        return room.rating()

    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user