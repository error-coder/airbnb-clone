from django.urls import path
from . import views


urlpatterns = [
    path("", views.Experiences.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/perks", views.ExperiencePerks.as_view()),
    path("<int:pk>/bookings", views.ExperienceBookings.as_view()),
    path(
        "<int:pk>/bookings/<int:booking_pk>", views.ExperienceBookingsDetail.as_view()
    ),
]
