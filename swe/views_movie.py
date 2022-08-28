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

    @swagger_auto_schema(
        operation_description="영화 등록(DB)",
        operation_id='영화 등록(DB)',
        tags=['movie'],
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
                data['poster_path'] = data['poster_path']
                data['release_date'] = datetime.strptime(data['release_date'], "%Y-%m-%d")
                data['movie'] = create_movie(data).pk
                data['creation_date'] = timezone.now()
                data['last_update_date'] = timezone.now()
                data['status'] = STATUS_ACTIVE

                for category in category_list:
                    category_data = copy.copy(data)
                    category_data['type_code'] = convert_category_to_code(category)
                    create_movie_meta(category_data)

            return Response(status=status.HTTP_201_CREATED)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="영화 조회수 증가",
        operation_id='영화 조회수 증가'
    )
    def update(self, request, movie_id):
        try:

            movie = Movie.objects.filter(id=movie_id)
            movie.update(
                last_update_date=timezone.now(),
                total_view=movie[0].total_view + 1,
                daily_view=movie[0].daily_view + 1,
            )

            return Response(status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="영화 조회",
        operation_id='영화 조회',
        manual_parameters=[access_token],
        tags=['movie'],
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
                                                     'comments': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                                                items=openapi.Items(
                                                                                    type=openapi.TYPE_OBJECT,
                                                                                    properties={
                                                                                        'is_mine': openapi.Schema(
                                                                                            type=openapi.TYPE_BOOLEAN),
                                                                                        'user_name': openapi.Schema(
                                                                                            type=openapi.TYPE_STRING),
                                                                                        'content': openapi.Schema(
                                                                                            type=openapi.TYPE_STRING),
                                                                                        'creation_date': openapi.Schema(
                                                                                            type=openapi.TYPE_STRING),
                                                                                    })),
                                                     'request_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                     'is_request': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                                 }
                                             )),
                })})
    def read(self, request, movie_id):
        try:
            user = get_user(request=request)
            result = dict()
            movie = Movie.objects.get(id=movie_id)
            result['title'] = movie.get_title
            result['director'] = movie.director
            result['release_date'] = movie.release_date
            # result['title'], result['director'], result['release_date'] = movie.movie_info_dto
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


class ViewMovieList(viewsets.GenericViewSet, mixins.ListModelMixin, View):
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
        description='검색 조건: title, director, genre',  # 쿼리 설명
        type=openapi.TYPE_STRING,
        example='title'
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    keyword = openapi.Parameter(
        'keyword',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='검색어',  # 쿼리 설명
        type=openapi.TYPE_STRING,
        example='아이언맨'
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
        operation_description="영화 리스트 조회",
        operation_id='영화 리스트 조회',
        manual_parameters=[keyword_type, keyword, page_size, page_count],
        tags=['movie'],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'page_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'page_size': openapi.Schema(type=openapi.TYPE_INTEGER),
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

            keyword_type = request.query_params.get('keyword_type', 'None')
            keyword = request.query_params.get('keyword', '')
            result['movies'] = list()
            movies_append = result['movies'].append

            if keyword_type == 'None':
                movies = Movie.objects.all().prefetch_related('movie_meta').order_by('id')

            elif keyword_type == 'title':
                movies = Movie.objects.filter(title__contains=keyword).prefetch_related('movie_meta').order_by(
                    'id')

            elif keyword_type == 'director':
                movies = Movie.objects.filter(director__contains=keyword).prefetch_related('movie_meta').order_by(
                    'id')

            elif keyword_type == 'genre':
                genre = convert_category_to_code(keyword)
                movies = Movie.objects.filter(movie_meta__type_code=genre).prefetch_related('movie_meta').order_by(
                    'id')

            paginator = Paginator(movies, page_size)  # 페이지당 page_size 개씩 보여주기
            page_obj = paginator.get_page(page_count)
            page_movies = page_obj.object_list

            result['total'] = paginator.count
            result['page_count'] = int(page_count)
            result['page_size'] = int(page_size)
            no = int(page_size) * (int(page_count) - 1) + 1

            for movie in page_movies:
                movie_data = dict()
                movie_data['no'] = no
                movie_data['movie_id'] = movie.id
                no += 1
                movie_data['title'] = movie.title
                movie_data['director'] = movie.director
                movie_data['release_date'] = movie.release_date
                movie_data['poster_path'] = POSTER_ROOT + movie.poster_path
                movie_data['category_list'] = convert_codes_to_name_list(
                    MovieMeta.objects.filter(movie=movie).values_list('type_code', flat=True))
                movies_append(movie_data)

            return Response(headers={'Location': 'swe/v1/movies'}, data=result, status=status.HTTP_302_FOUND)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)
