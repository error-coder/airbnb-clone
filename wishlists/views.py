from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from .models import Wishlist
from .serializers import WishlistSerializer
from common.views import get_object, check_owner
from rooms.models import Room


class Wishlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)

        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = WishlistSerializer(
                wishlist,
                context={"request": request},
            )
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        wishlist = get_object(Wishlist, pk)
        check_owner(request, wishlist.user)

        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = get_object(Wishlist, pk)
        check_owner(request, wishlist.user)

        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        wishlist = get_object(Wishlist, pk)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(
                wishlist,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistRoomToggle(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, room_pk):
        wishlist = get_object(Wishlist, pk)
        check_owner(request, wishlist.user)
        room = get_object(Room, room_pk)

        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)

        else:
            wishlist.rooms.add(room)

        return Response(status=HTTP_200_OK)