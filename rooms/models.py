from django.db import models
from common.models import CommonModel

class Room(CommonModel):

    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_rooms", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(max_length=180, default="",)
    country = models.CharField(max_length=50, default="한국",)
    city = models.CharField(max_length=80, default="서울",)
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=20, choices=RoomKindChoices.choices,)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE,)
    amenities = models.ManyToManyField("rooms.Amenity")
    category = models.ForeignKey("categories.Category", null=True, blank=True, on_delete=models.SET_NULL,)
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add는 필드의 값을 해당 object가 처음 생성되었을 때 시간으로 설정함 -> room이 만들어지면 django는 이 방이 만들어진 date를 이 부분에 넣음
    updated_at = models.DateTimeField(auto_now=True) # auto_now는 저장될 때마다 해당 필드를 현재 date로 설정함

    def __str__(room) -> str:
        return room.name

    def total_amenities(room):
        return room.amenities.count()

class Amenity(CommonModel):

    """Amenity Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, default="", blank=True)

    def __str__(self) -> str:
        return self.name