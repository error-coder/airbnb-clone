from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated
from rooms.models import Room
from .models import Wishlist
from .serializers import WishlistSerializer


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)

        return Response(
            WishlistSerializer(
                wishlists,
                many=True,
                context={"request": request},
            ).data,
        )

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)

        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            return Response(WishlistSerializer(wishlist).data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )

        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistToggle(APIView):

    permission_classes = [IsAuthenticated]

    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Wishlist.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)

        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)

        return Response(status=HTTP_204_NO_CONTENT)
