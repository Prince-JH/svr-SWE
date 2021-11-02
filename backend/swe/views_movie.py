import copy
import traceback
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from config.settings.dev import POSTER_ROOT
from swe.func import create_member, create_movie, create_movie_meta, convert_category_to_code, \
    convert_codes_to_name_list
from swe.globals import *
from swe.models import Member, Movie, Code, MovieMeta


class ViewMovie(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    """
    영화
    """
    access_token = openapi.Parameter(
        'access-token',  # 쿼리 이름
        openapi.IN_HEADER,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='ACCESS_TOKEN',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    keyword_type = openapi.Parameter(
        'keyword_type',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='keyword_type',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    keyword = openapi.Parameter(
        'keyword',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='keyword',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    page_count = openapi.Parameter(
        'page_count',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='page_count',  # 쿼리 설명
        type=openapi.TYPE_INTEGER
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    page_size = openapi.Parameter(
        'page_size',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='page_size',  # 쿼리 설명
        type=openapi.TYPE_INTEGER
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )

    @swagger_auto_schema(
        operation_description="영화 등록",
        operation_id='save movie',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'director': openapi.Schema(type=openapi.TYPE_STRING),
                'release_date': openapi.Schema(type=openapi.TYPE_STRING),
                'poster_path': openapi.Schema(type=openapi.TYPE_STRING),
                'category_list': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                items=openapi.Items(
                                                    type=openapi.TYPE_STRING))
            }))
    def create(self, request):
        try:
            with transaction.atomic():
                data = request.data
                category_list = data['category_list']
                data['poster_path'] = POSTER_ROOT + data['poster_path']
                data['release_date'] = datetime.strptime(data['release_date'], "%Y-%m-%d")
                data['movie'] = create_movie(data).pk
                data['creation_date'] = timezone.now()
                data['last_update_date'] = timezone.now()


                for category in category_list:
                    category_data = copy.copy(data)
                    category_data['type_code'] = convert_category_to_code(category)
                    create_movie_meta(category_data)

            return Response(status=status.HTTP_201_CREATED)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="영화 수정",
        operation_id='sign in, sign out',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            }),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING),
                    }))}
    )
    def update(self, request):
        try:
            data = request.data
            user = User.objects.get(username=data['email'])
            member = Member.objects.filter(email=data['email'], status=STATUS_ACTIVE)
            if check_password((data['password']), user.password):
                result = dict()
                token = Token.objects.get_or_create(user=user)[0].key
                result['token'] = token
                member.update(
                    access_token=token,
                    last_update_date=timezone.now()
                )
            else:
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

            return Response(data=result, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="영화 조회",
        operation_id='check existence',
        manual_parameters=[keyword_type, page_size, page_count],
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
                                                                                         type=openapi.TYPE_STRING))
                                                 }
                                             )),
                })})
    def read(self, request):
        try:
            result = dict()

            page_size = request.query_params.get("page_size", 10)
            page_count = request.query_params.get("page_count", 1)

            keyword_type = request.query_params.get('keyword_type', 'All')
            result['movies'] = list()
            movies_append = result['movies'].append

            if keyword_type == 'All':

                movies = Movie.objects.all().prefetch_related('movie_meta').order_by('daily_view')
                paginator = Paginator(movies, page_size)  # 페이지당 page_size 개씩 보여주기
                page_obj = paginator.get_page(page_count)
                page_movies = page_obj.object_list

                for movie in page_movies:
                    movie_data = dict()
                    movie_data['title'] = movie.title
                    movie_data['director'] = movie.director
                    movie_data['release_date'] = movie.release_date
                    movie_data['poster_path'] = POSTER_ROOT + movie.poster_path
                    movie_data['category_list'] = convert_codes_to_name_list(
                        MovieMeta.objects.filter(movie=movie).values_list('type_code', flat=True))
                    movies_append(movie_data)

            return Response(data=result, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)
