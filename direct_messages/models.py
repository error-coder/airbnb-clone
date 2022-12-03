from django.db import models
from common.models import CommonModel

class ChattingRoom(CommonModel):

    """Room Model Definition"""

    users = models.ManyToManyField("users.User",)

    def __str__(self) -> str:
        return "Chatting Room."

class Message(CommonModel):

    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL,) # 유저만 삭제되고 보낸 메시지 내용은 삭제도지 않음
    room = models.ForeignKey("direct_messages.ChattingRoom", on_delete=models.CASCADE,) # 방이 삭제되면 메시지도 같이 삭제됨

    def __str__(self) -> str:
        return f"{self.user} says : {self.text}"