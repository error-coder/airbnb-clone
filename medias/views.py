import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated
from common.views import get_object, check_owner
from .models import Photo


class GetUploadURL(APIView):
    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUD_FLARE_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CLOUD_FLARE_TOKEN}",
            },
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        return Response({"uploadURL": result.get("uploadURL")})


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        photo = get_object(Photo, pk)

        if photo.room:
            check_owner(request, photo.room.owner)
        elif photo.experience:
            check_owner(request, photo.experience.host)

        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)