from django.db import models
from django.core.validators import MinValueValidator
from common.models import CommonModel
from users.models import User
from categories.models import Category


class Perk(CommonModel):
    """ "What is included on an Experience"""

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
    )
    explanation = models.TextField(
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class Experience(CommonModel):
    """Experience Model Definition"""

    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=18,
        default="서울",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
    )
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(Perk)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
    )

    def __str__(self) -> str:
        return self.name

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]

            return f"{round(total_rating / count,2)}"