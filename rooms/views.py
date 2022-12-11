from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Amenity
from .serializers import AmenitySerializer

class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 사용자의 데이터로 serializer를 만들 때는 serializer는 사용자의 데이터가 amenity object가 원하는 데이터에 준수하는지 검증해야 함
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            # True일 경우 serializer.save를 해서 ModelSerializer가 자동으로 amenity를 만들게 해야함
            amenity = serializer.save()
            # 새로 만들어진 것을 serialize한 다음 리턴해줌
            return Response(AmenitySerializer(amenity).data,)
        else:
            return Response(serializer.errors)

class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound


    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        # partial은 부분 업데이트로 name 또는 description을 변경할 수 있음(둘 다X, 둘 중에 하나)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True,)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data,)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)