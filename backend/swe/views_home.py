import copy
import traceback
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from config.settings.dev import POSTER_ROOT
from swe.func import create_member, create_movie, create_movie_meta, convert_category_to_code, \
    convert_codes_to_name_list, get_user
from swe.globals import *
from swe.models import Member, Movie, Code, MovieMeta, Request, Comment


class ViewHome(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    """
    홈
    """
    top_count = openapi.Parameter(
        'top_count',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='top 몇?',  # 쿼리 설명
        type=openapi.TYPE_INTEGER,
        example=3
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    keyword = openapi.Parameter(
        'keyword',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='age or address or profession',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    @swagger_auto_schema(
        operation_description="TOP 조회",
        operation_id='TOP 조회',
        manual_parameters=[top_count, keyword],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'movies': openapi.Schema(type=openapi.TYPE_ARRAY,
                                             items=openapi.Items(
                                                 openapi.TYPE_OBJECT,
                                                 properties={
                                                     'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                     'director': openapi.Schema(type=openapi.TYPE_STRING),
                                                     'release_date': openapi.Schema(type=openapi.TYPE_STRING),
                                                     'poster_path': openapi.Schema(type=openapi.TYPE_STRING),
                                                     'category_list': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                                                     items=openapi.Items(
                                                                                         type=openapi.TYPE_STRING)),
                                                     'request_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                     'is_request': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                                 }
                                             )),
                })})
    def read(self, request, movie_id):
        try:
            user = get_user(request=request)
            keyword = request.query_params.get('keyword', None)

            # if keyword is None:
            result = dict()
            movie = Movie.objects.get(id=movie_id)
            result['title'] = movie.title
            result['director'] = movie.director
            result['release_date'] = movie.release_date
            result['poster_path'] = POSTER_ROOT + movie.poster_path
            result['category_list'] = convert_codes_to_name_list(
                MovieMeta.objects.filter(movie=movie).values_list('type_code', flat=True))
            result['comments'] = list()
            comments_append = result['comments'].append
            comments = Comment.objects.select_related('user').filter(movie=movie, status=STATUS_ACTIVE)
            for comment in comments:
                comment_data = dict()
                comment_data['comment_id'] = comment.id
                comment_data['user_name'] = comment.user.name
                comment_data['content'] = comment.content
                comment_data['creation_date'] = comment.creation_date
                comment_data['is_mine'] = True if comment.user == user else False
                comments_append(comment_data)
            # result['comments'] = Comment.objects.filter(movie=movie, status=STATUS_ACTIVE).annotate(
            #     user_name=F('user__name'), is_mine=F('True')).values('id', 'user_name', 'content', 'creation_date', 'is_mine')
            result['request_count'] = Request.objects.filter(movie=movie, status=STATUS_ACTIVE).count()
            result['is_request'] = True if Request.objects.filter(movie=movie, status=STATUS_ACTIVE,
                                                                  user=user).count() > 0 else False

            return Response(data=result, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)