from django.urls import path

from swe.views_comments import ViewComment
from swe.views_home import ViewHome
from swe.views_movie import ViewMovie, ViewMovieList
from swe.views_request import ViewRequest
from swe.views_user import UserSign, UserInfo

urlpatterns = [
    path('swe/v1/user', UserSign.as_view({"post": "create", "put": "update", "get": "read"}), name='user-sign'),
    path('swe/v1/user/info', UserInfo.as_view({"get": "read"}), name='user-info'),
    path('swe/v1/movie', ViewMovie.as_view({"post": "create"}), name='movie'),
    path('swe/v1/movie/<movie_id>', ViewMovie.as_view({"put": "update", "get": "read"}), name='movie'),
    path('swe/v1/movie-list', ViewMovieList.as_view({"get": "read"}), name='movie-list'),

    path('swe/v1/comments', ViewComment.as_view({"post": "create"}), name='comments'),
    path('swe/v1/comments/<comment_id>', ViewComment.as_view({"put": "update"}), name='comments'),

    path('swe/v1/request', ViewRequest.as_view({"post": "create"}), name='request'),
    path('swe/v1/home', ViewHome.as_view({"get": "read"}), name='home')

]
