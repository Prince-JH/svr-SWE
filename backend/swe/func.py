from swe.models import Code
from swe.models_serializer import SerializerMember, SerializerMovie, SerializerMovieMeta


def convert_category_to_code(category):
    return Code.objects.get(name=category).code


def create_member(data):
    user = SerializerMember(data=data)
    user.is_valid(raise_exception=True)
    user.save()


def create_movie(data):
    movie = SerializerMovie(data=data)
    movie.is_valid(raise_exception=True)
    return movie.save()


def create_movie_meta(data):
    movie_meta = SerializerMovieMeta(data=data)
    movie_meta.is_valid(raise_exception=True)
    movie_meta.save()
