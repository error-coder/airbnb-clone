"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from strawberry.django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v3/rooms/", include("rooms.urls")),
    path("api/v3/categories/", include("categories.urls")), # api를 나타내는 새로운 url 이름을 지어줌(버전까지 나타내주는 것도 중요)
    path("api/v3/experiences/", include("experiences.urls")),
    path("api/v3/medias/", include("medias.urls")),
    path("api/v3/wishlists/", include("wishlists.urls")),
    path("api/v3/users/", include("users.urls")),
    path("graphql", GraphQLView.as_view(schema=schema)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)