import strawberry
from strawberry import auto
from . import models


@strawberry.django.type(models.Category)
class CategoryType:
    name: auto
    kind: auto
