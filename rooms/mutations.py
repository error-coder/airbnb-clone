import typing
import strawberry
from enum import Enum
from strawberry.types import Info
from django.db import transaction
from categories.models import Category
from rooms.models import Amenity, Room


def check_Category(category_pk):
    try:
        category = Category.objects.get(pk=category_pk)
        if category.kind == Category.CategoryKindChoices.EXPERIENCES:
            raise Exception("The category kind should be 'rooms'")
        return category

    except Category.DoesNotExist:
        raise Exception("Category not found")


def add_amenities(amenities, room):
    try:
        for amenity_pk in amenities:
            amenity = Amenity.objects.get(pk=amenity_pk)
            room.amenities.add(amenity)
    except Exception:
        raise Exception("Amenity not found")


@strawberry.enum
class RoomKindChoices(Enum):
    ENTIRE_PLACE = "entire_place"
    PRIVATE_ROOM = "private_room"
    SHARED_ROOM = "shared_room"


@strawberry.input
class PostRoomInput:
    name: str
    country: typing.Optional[str] = None
    city: typing.Optional[str] = None
    price: int
    rooms: int
    toilets: int
    description: str
    address: str
    pet_friendly: typing.Optional[str] = None
    kind: RoomKindChoices
    amenities: typing.Optional[typing.List[int]] = None
    category: int


def post_room(
    info: Info,
    data: PostRoomInput,
):
    category = check_Category(category_pk=data.category)

    with transaction.atomic():
        try:
            room = Room.objects.create(
                name=data.name,
                price=data.price,
                rooms=data.rooms,
                toilets=data.toilets,
                description=data.description,
                address=data.address,
                kind=data.kind,
                owner=info.context.request.user,
                category=category,
            )

        except Exception as inst:
            if f"{inst.__cause__}" == "CHECK constraint failed: price":
                raise Exception("Price 값을 확인해주세요")

        if data.pet_friendly:
            room.pet_friendly = data.pet_friendly

        if data.country:
            room.country = data.country

        if data.city:
            room.city = data.city

        room.save()

        if data.amenities:
            add_amenities(data.amenities, room)

        return room