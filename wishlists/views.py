from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rooms.models import Room
from .models import Wishlist
from .serializers import WishlistSerializer

class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user) # 동일한 유저가 갖고 있는 위시리스트만 찾기 위해 filter 사용
        serializer = WishlistSerializer(all_wishlists, many=True, context={"request" : request},)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user,) # 호출될 때 모델(위시리스트)을 받음
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated ]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist, context={"request" : request},)
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)
    
    def put(self, request, pk): # user가 wishlist의 이름만 변경할 수 있음
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist, data=request.data, partial=True,)
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist, context={"request" : request},)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistToggle(APIView):

    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk ,request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room_pk).exists(): 
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)

# def put(self, request, pk, room_pk):
#         wishlist = self.get_list(pk ,request.user)
#         room = self.get_room(room_pk)
#         if wishlist.rooms.filter(pk=room_pk).exists(): 
#             wishlist.rooms.remove(room)
#         else:
#             wishlist.rooms.add(room)
#         return Response(status=HTTP_200_OK)

# ManyToManyField(room의 list)로 들어가서 wishlist 내부의 roomlist로 접근해서 filter, db에서 room의 pk랑 일치하는 pk를 갖는 room이 있는지 확인
# room pk는 user가 url에 적은 room_pk로부터 확인 가능
# wishlist.rooms이 user가 등록, 삭제하려는 pk랑 일치하는 방을 갖고 있는지 확인하는 것
# 그냥 조건에 맞는 list만 반환하는 filter() 대신 exists()를 추가해 존재하는지 확인할 수 있음
# list에 room이 있으면, list에서 그 room을 지울 거고 그렇지 않으면 추가함