from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("token-login", obtain_auth_token), # username과 password를 보내면 token 반환
    path("jwt-login", views.JWTLogin.as_view()),
    path("@<str:username>", views.PublicUser.as_view()), # 위 코드보다 먼저 쓰면 username을 me로 보기 때문에 에러 발생
]