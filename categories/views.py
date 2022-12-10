from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

@api_view(["GET", "POST"])
def categories(request):

    if request.method == "GET":
        all_categories = Category.objects.all()
        # serializer가 헷갈리지 않게 serializer에게 많은 카테고리를 보낸다고 알림
        serializer = CategorySerializer(all_categories, many=True) 
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save() # serializer 안에 있던 검증된 데이터로 create 메서드를 호출함
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)

@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)