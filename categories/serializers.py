from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__" # 필드도 마음대로 선택하거나 제외할 수도 있음