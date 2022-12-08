from django.contrib import admin
from .models import Room, Amenity

@admin.action(description="Set all prices to zero")

# action은 3개의 매개변수가 반드시 필요함
# model_admin은 액션을 호출한 클래스
# request 객체는 이 액션을 호출한 유저 정보를 갖고 있음
# rooms(queryset) 선택된 방에 대한 내용을 갖고 있음
def reset_prices(model_admin, request, rooms): 
    for room in rooms.all():
        room.price = 0
        room.save()
    

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    # list_display에서 모델의 속성 뿐만 아니라 메소드도 적을 수 있음
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
    )

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
    )

    # ^(startswoth) ->시작하는 단어로 검색하고 싶음
    # =(exact)는 완전히 동일한 것으로 검색하고 싶음
    # 아무것도 적지 않으면 contains
    search_fields = ("name", "^price", "=owner__username",) 

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
