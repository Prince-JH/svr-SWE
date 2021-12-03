import copy
import operator
import traceback
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Count
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


class ViewAdmin(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    """
    관리자
    """
    access_token = openapi.Parameter(
        'access-token',  # 쿼리 이름
        openapi.IN_HEADER,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='ACCESS_TOKEN',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
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
        description='age or address or sex',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    keyword_value = openapi.Parameter(
        'keyword_value',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='선택한 키워드의 값: 20(20대), 30(30대), 40(40대), 강남구, 관악구, 서대문구, 동작구, M, F',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )

    @swagger_auto_schema(
        operation_description="통계 조회",
        operation_id='통계 조회',
        manual_parameters=[access_token, top_count, keyword, keyword_value],
        tags=['admin'],
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
    def read(self, request):
        try:
            user = get_user(request=request)
            if user.role != 'admin':
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            keyword = request.query_params.get('keyword', None)
            keyword_value = request.query_params.get('keyword_value', None)
            top_count = int(request.query_params.get('top_count', 5))

            result = dict()
            result['movies'] = list()

            if keyword is not None:
                if keyword == 'age':
                    target_age = int(keyword_value)
                    requests = list(
                        Request.objects.select_related('movie').filter(user__age__startswith=target_age // 10,
                                                                       status=STATUS_ACTIVE).values(
                            'movie').annotate(count=Count('movie')))
                elif keyword == 'address':
                    target_address = keyword_value
                    dong = target_address[1]
                    requests = list(
                        Request.objects.select_related('movie').filter(user__address__contains=dong,
                                                                       status=STATUS_ACTIVE).values(
                            'movie').annotate(count=Count('movie')))
                elif keyword == 'sex':
                    target_sex = keyword_value
                    requests = list(
                        Request.objects.select_related('movie').filter(user__sex=target_sex,
                                                                       status=STATUS_ACTIVE).values(
                            'movie').annotate(count=Count('movie')))
                if len(requests) > 0:
                    requests.sort(key=(operator.itemgetter('count')), reverse=True)

                    target_movies = [requests[no]['movie'] for no in range(top_count)] if len(
                        requests) > top_count else [requests[no]['movie'] for no in range(len(requests))]

                    movies = Movie.objects.filter(id__in=target_movies)
                    for movie in movies:
                        movie_data = dict()
                        movie_data['movie_id'] = movie.id
                        movie_data['title'] = movie.title
                        movie_data['director'] = movie.director
                        movie_data['release_date'] = movie.release_date
                        movie_data['poster_path'] = POSTER_ROOT + movie.poster_path
                        movie_data['category_list'] = convert_codes_to_name_list(
                            MovieMeta.objects.filter(movie=movie).values_list('type_code', flat=True))
                        movie_data['request_count'] = Request.objects.filter(movie=movie, status=STATUS_ACTIVE).count()
                        movie_data['is_request'] = True if Request.objects.filter(movie=movie, status=STATUS_ACTIVE,
                                                                                  user=user).count() > 0 else False
                        result['movies'].append(movie_data)
                    result['movies'].sort(key=(operator.itemgetter('request_count')), reverse=True)

            return Response(data=result, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)
