from django.db import models
from common.models import CommonModel

class Review(CommonModel):

    """Review from a User to a Room or Experience"""

    # Reviews는 한번의 experience를 가짐
    # experience는 많은 reviews를 가질 수 있음

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews",)
    room = models.ForeignKey("rooms.Room", null=True, blank=True, on_delete=models.SET_NULL, related_name="reviews",)
    experience = models.ForeignKey("experiences.Experience", null=True, blank=True, on_delete=models.CASCADE, related_name="reviews",)
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐"