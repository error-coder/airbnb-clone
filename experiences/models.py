from django.db import models
from common.models import CommonModel

class Experience(CommonModel):

    """Experience model Definition"""

    country = models.CharField(max_length=50, default="한국",)
    city = models.CharField(max_length=80, default="서울",)
    name = models.CharField(max_length=250,)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE,)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250,)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk",)

    # cascade는 카테고리가 삭제되면 이 experiences도 삭제된다는걸 말함
    # SET_NULL은 categories의 category가 삭제되면 experiences의 카테고리를 null로 만듦
    category = models.ForeignKey("categories.Category", null=True, blank=True, on_delete=models.SET_NULL,)


    def __str__(self) -> str:
        return self.name
    
class Perk(CommonModel):

    """What is included on an Experience"""

    name = models.CharField(max_length=100,)
    details = models.CharField(max_length=250, blank=True, default="",)
    explanation = models.TextField(blank=True, default="",)

    def __str__(self) -> str:
        return self.name