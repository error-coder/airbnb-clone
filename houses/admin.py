from django.contrib import admin
from .models import House

@admin.register(House) # HouseAdmin 클래스가 House model을 통제할 것임

# HouseAdmin 클래스는 ModelAdmin 클래스로부터 모든 걸 상속받음
class HouseAdmin(admin.ModelAdmin):
    fields = ("name", "address", "price_per_night", "pets_allowed")
    list_display = ("name", "price_per_night", "address", "pets_allowed")        
    list_filter = ("price_per_night", "pets_allowed")
    # 튜플이 있고 그 안에 한개의 원소밖에 없다면 string으로 인식함 -> 콤마를 뒤에 붙여줘야함
    search_fields = ("address",)
    list_display_links = ("name", "address")
    list_editable = ("pets_allowed",)