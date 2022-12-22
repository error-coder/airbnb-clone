from . import models

def get_all_rooms(): # Information으로 user가 authenticated인지 아닌지 알 수 있음
        return models.Room.objects.all()
    

def get_room(pk:int):
    try:
        return models.Room.objects.get(pk=pk)
    except models.Room.DoesNotExist:
        return None