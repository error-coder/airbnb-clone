from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.Serializer):
    # 카테고리 필드 중에 어떤 부분을 보여줄지 명시해야함
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=50,)
    kind = serializers.ChoiceField(choices=Category.CategoryKindChoices.choices,)
    created_at = serializers.DateTimeField(read_only=True)

    # 객체는 직접 다뤄야 함
    def create(self, validated_data):
        return Category.objects.create(**validated_data)
        
        # **는 딕셔너리를 가져옴
        # name = 'Category from DRF'
        # kind - 'rooms'로 자동으로 바꿔줌

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.kind = validated_data.get('kind', instance.kind)
        instance.save() 
        return instance