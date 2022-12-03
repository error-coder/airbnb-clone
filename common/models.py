from django.db import models

class CommonModel(models.Model):

    """"Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 이 class는 djagno에서 model을 configure할 때 사용함
    # abstract model -> django가 이 model을 봐도 db에 저장안함(데이터로 사용x)
    class Meta:
        abstract = True