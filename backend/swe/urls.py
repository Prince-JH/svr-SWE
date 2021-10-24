from django.urls import path

from swe.views_movie import Movie
from swe.views_user import UserSign

urlpatterns = [
    path('swe/v1/user', UserSign.as_view({"post": "create", "put": "update", "get": "read"}), name='user-sign'),
    path('swe/v1/movie', Movie.as_view({"post": "create"}), name='movie')
]
