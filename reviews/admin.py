from django.contrib import admin
from .models import Review

# 커스텀 필터를 만드려면 admin.SimpleListFilter를 상속받는 클래스를 만들어야함
# 2가지를 명시해야함
# parameter_name은 url에 표시됨
class WordFilter(admin.SimpleListFilter):

    title = "Filter by words!"

    parameter_name = 'word'

    # lookups와 queryset 2가지 메소드를 만들어야함
    # lookups은 튜플의 리스트를 리턴해야 하는 함수, 튜플의 첫번째 요소는 url에 나타남, 두번째 요소는 유저가 보고 클릭하게 되는 텍스트임
    # queryset은 필터링된 review를 리턴해야 하는 메소드
    # url에 있는 값을 가져오기 위해 self.value를 호출하기만 하면 됨
    def lookups(self, request, model_admin):
        return [("good", "Good"), ("great", "Great"), ("awesome","Awesome"),]

    def queryset(self, request, reviews):
        # url에 보이는 word를 줌
        word = self.value()
        if word:
            # payload에 word를 포함하는 review를 필터링함, word는 url안에 있던 것
            return reviews.filter(payload__contains=word)
        # 만약 url에 어떠한 단어가 없어도 모든 리뷰를 리턴하도록 해야 함 -? '모두'라는 필터를 선택했을 때 발생
        else:
            reviews

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = ("__str__", "payload",)
    list_filter = (WordFilter,"rating","user__is_host","room__category","room__pet_friendly",)