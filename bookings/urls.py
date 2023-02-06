from django.urls import path
from . import views

urlpatterns = [
    path("me", views.GetMyBookings.as_view()),
    path("manage", views.ManageBookings.as_view()),
    path("me/<int:pk>/cancel", views.CancelMyBooking.as_view()),
]
