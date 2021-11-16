from django.db import transaction

from swe.models import Code, Member
from swe.models_serializer import SerializerMember, SerializerMovie, SerializerMovieMeta, SerializerComment, \
    SerializerRequest


def convert_category_to_code(category):
    return Code.objects.get(name=category).code


def convert_codes_to_name_list(codes):
    return Code.objects.filter(code__in=codes).values_list('name', flat=True)


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


def create_comment(data):
    comment = SerializerComment(data=data)
    comment.is_valid(raise_exception=True)
    comment.save()


def create_request(data):
    request = SerializerRequest(data=data)
    request.is_valid(raise_exception=True)
    return request.save()


def get_user(*args, **kwargs):
    print("get_user_info")
    try:

        with transaction.atomic():
            if 'request' in kwargs:
                request = kwargs['request']
                if request.META.get('HTTP_ACCESS_TOKEN') is not None:
                    user = Member.objects.get(access_token=request.META.get('HTTP_ACCESS_TOKEN'))
            elif 'access_token' in kwargs:
                access_token = kwargs['access_token']
                user = Member.objects.get(access_token=access_token)
            elif 'user_id' in kwargs:
                user_id = kwargs['user_id']
                user = Member.objects.get(pk=user_id)
            return user

    except Exception as err:
        print('err:get_user_info', err)
        # ret_code = status.HTTP_400_BAD_REQUEST
        return None
