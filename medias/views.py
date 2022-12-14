from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Photo

class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        # 만약 사진이 방을 가지고 주인이 있고 주인이 요청한 유저와 다르다면 권한 거부
        # 사진이 경험을 가지고 있고 경험의 주인과 요청 보낸 유저가 다르다면 권한 거부
        if (photo.room and photo.room.owner != request.user) or (photo.experience and photo.experience.host != request.user):
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)

# 유저가 인증되야 하는 APIView에서 인증을 확인하지 않아도 가능하게 할 수 있음

