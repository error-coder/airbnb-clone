from django.urls import path
from . import views
from .views import Perks, PerkDetail, Experiences, ExperienceDetail, ExperienceBookings, ExperienceBookingDetail

urlpatterns = [
    path("", views.Experiences.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/perks", views.ExperiencePerks.as_view()),
    path("<int:pk>/bookings", views.ExperienceBookings.as_view()),
    path("<int:pk>/bookings/<int:booking_pk>", views.ExperienceBookingDetail.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),   
]