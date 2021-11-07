from django.urls import path

from swe.views_comments import ViewComment
from swe.views_movie import ViewMovie, ViewMovieList
from swe.views_user import UserSign

urlpatterns = [
    path('swe/v1/user', UserSign.as_view({"post": "create", "put": "update", "get": "read"}), name='user-sign'),
    path('swe/v1/movie', ViewMovie.as_view({"post": "create"}), name='movie'),
    path('swe/v1/movie/<movie_id>', ViewMovie.as_view({"put": "update", "get": "read"}), name='movie'),
    path('swe/v1/movie-list', ViewMovieList.as_view({"get": "read"}), name='movie-list'),

    path('swe/v1/comments', ViewComment.as_view({"post": "create"}), name='comments'),
    path('swe/v1/comments/<comment_id>', ViewComment.as_view({"put": "update"}), name='comments')

]
