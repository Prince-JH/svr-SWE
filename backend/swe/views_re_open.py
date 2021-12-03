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
    convert_codes_to_name_list, get_user, create_comment, create_request, create_re_open
from swe.globals import *
from swe.models import Member, Movie, Code, MovieMeta, Request, Comment, ReOpen


class ViewReOpen(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    """
    재개봉
    """
    access_token = openapi.Parameter(
        'access-token',  # 쿼리 이름
        openapi.IN_HEADER,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='ACCESS_TOKEN',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )

    @swagger_auto_schema(
        operation_description="재개봉 확정",
        operation_id='재개봉 확정',
        tags=['re-open'],
        manual_parameters=[access_token],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'movie_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }))
    def create(self, request):
        try:
            user = get_user(request=request)
            if user is None or user.role != 'admin':
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            with transaction.atomic():
                data = request.data
                data['movie'] = data['movie_id']
                data['status'] = STATUS_ACTIVE
                data['creation_date'] = timezone.now()
                data['last_update_date'] = timezone.now()
                create_re_open(data).pk

            return Response(status=status.HTTP_201_CREATED)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="재개봉 리스트 조회",
        operation_id='재개봉 리스트 조회',
        tags=['re-open'],
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
                                                     're-open_date': openapi.Schema(type=openapi.TYPE_STRING)
                                                 }
                                             )),
                })})
    def read(self, request):
        try:

            result = dict()
            result['movies'] = list()
            movies_append = result['movies'].append

            reopens = ReOpen.objects.select_related('movie').filter(status=STATUS_ACTIVE)
            for reopen in reopens:
                movie_data = dict()
                movie_data['movie_id'] = reopen.movie.id
                movie_data['title'] = reopen.movie.title
                movie_data['director'] = reopen.movie.director
                movie_data['release_date'] = reopen.movie.release_date
                movie_data['poster_path'] = POSTER_ROOT + reopen.movie.poster_path
                movie_data['category_list'] = convert_codes_to_name_list(
                    MovieMeta.objects.filter(movie=reopen.movie).values_list('type_code', flat=True))
                movies_append(movie_data)
                movie_data['re-open_date'] = reopen.creation_date

            return Response(data=result, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)
