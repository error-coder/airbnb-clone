from django.db import models
from common.models import CommonModel
from rooms.models import Room
from experiences.models import Experience


class Photo(CommonModel):
    file = models.URLField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        Room,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    experience = models.ForeignKey(
        Experience,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    def __str__(self) -> str:
        return "Photo File"


class Video(CommonModel):
    file = models.URLField()
    experience = models.OneToOneField(
        Experience,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "Video File"