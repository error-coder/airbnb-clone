from django.db import models
from common.models import CommonModel
from users.models import User
from rooms.models import Room
from experiences.models import Experience


class Review(CommonModel):
    """Review from a User to a Room or Experience"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    room = models.ForeignKey(
        Room,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    experience = models.ForeignKey(
        Experience,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐️"