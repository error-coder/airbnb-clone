from django.db import models
from common.models import CommonModel

class Photo(CommonModel):

    file = models.URLField()
    description = models.CharField(max_length=140,)
    room = models.ForeignKey("rooms.Room",null=True, blank=True, on_delete=models.CASCADE, related_name="photos",)
    experience = models.ForeignKey("experiences.Experience",null=True, blank=True, on_delete=models.CASCADE, related_name="photos",)

    def __str__(self):
        return "Photo File"

class Video(CommonModel):

    file = models.URLField()
    experience = models.OneToOneField("experiences.Experience", on_delete=models.CASCADE, related_name="videos",) # 한 개의 활동이 여러 동영상을 가질 수 없음

    def __str__(self):
        return "Video File"