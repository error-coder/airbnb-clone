from django.db import models
from django.contrib.auth.models import AbstractUser

# models.py를 수정할 때마다 migratiob을 만들고 migrate 해야함
# 코드에 있는 모델 구조와 db 구조를 서로 동기화 하기 위해서임

class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English") # db 값은 max_length 값보다 작아야함
    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "Dollar"

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    avatar = models.URLField(blank=True,) # blank=True는 form에서 필드가 필수적이지 않게 해줌
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False) # 모든 사용자는 is_host 값을 False로 받게됨
    gender = models.CharField(max_length=10, choices=GenderChoices.choices,)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices,)
    currency = models.CharField(max_length=5, choices=CurrencyChoices.choices,)