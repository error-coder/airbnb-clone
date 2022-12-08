from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# 모든 정보는 request에 들어있고 url에 요청을 보내고있는 유저의 정보도 자동으로 request objects안에 넣어줌
def see_all_rooms(request):
    rooms = Room.objects.all()
    # 딕셔너리를 만들어 key와 value로 어떤 것이든 넘겨줄 수 있음
    return render(request, "all_rooms.html", {'rooms': rooms, "title" : "Hello! this tilte comes from the django!",},)

def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(request, "room_detail.html", {'room': room,},)
    except Room.DoesNotExist:
        return render(request, "room_detail.html", {"not_found" : True,},)

# 방이 존재하지 않으면 room_detail을 렌더링 하는데 not_found:True라는 변수를 넘겨줌
# not_found가 False라면, room_detail에 있는 정보들을 보여줌, not_found가 True면 404를 보여줌