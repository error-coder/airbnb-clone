from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    # 카테고리 필드 중에 어떤 부분을 보여줄지 명시해야함
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=50,)
    kind = serializers.CharField(max_length=15,)
    created_at = serializers.DateTimeField(read_only=True)