from django.urls import path
from . import views

urlpatterns = [
    path("", views.see_all_rooms),
    path("<int:room_pk>", views.see_one_room),
    # 빈문자로 적어준건 이 url은 /rooms url로 들어온 url 이기 때문
    # ""  = /rooms
    # <> 안에 받아올 parameter의 타입을 적어줘야 함
]