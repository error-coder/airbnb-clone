from django.contrib import admin
from .models import Review


class RatingFilter(admin.SimpleListFilter):

    parameter_name = "input_rating"
    title = "Filter by rating"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, reviews):
        rating = request.GET.get("input_rating")
        if rating == "good":
            return reviews.filter(rating__gte=3)
        elif rating == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ("__str__", "payload")

    list_filter = (
        "rating",
        RatingFilter,
    )
