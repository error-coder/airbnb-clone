from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    # Viewset은 두 가지를 알아야함
    # serializer가 뭔지 알아야 하고 Viewset의 object가 뭔지 알아야함, 사용하기에 좋지는 않음
    serializer_class = CategorySerializer
    queryset = Category.objects.all()