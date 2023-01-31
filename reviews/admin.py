from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):

    title = "Filter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews


class GoodOrBadFilter(admin.SimpleListFilter):

    title = "Good or bad filter!"

    parameter_name = "state"

    def lookups(self, request, model_admin):
        return [
            ("good", "Is Good"),
            ("bad", "Is Bad"),
        ]

    def queryset(self, request, reviews):
        value = self.value()

        if value == "good":
            return reviews.filter(rating__gte=3)
        elif value == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
