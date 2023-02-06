from django.urls import path
from . import views


urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>", views.RoomDetial.as_view()),
    path("<int:pk>/amenities", views.RoomAmenities.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("<int:pk>/bookings", views.RoomBookings.as_view()),
    path("<int:pk>/bookings/check", views.RoomBookingCheck.as_view()),
    path("<int:pk>/bookings/<int:booking_pk>", views.RoomBookingDetail.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),        
]