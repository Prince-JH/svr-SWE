import copy
import traceback

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.utils import timezone
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from swe.func import create_member, create_movie, create_movie_meta, convert_category_to_code
from swe.globals import *
from swe.models import Member


class Movie(viewsets.GenericViewSet, mixins.ListModelMixin, View):
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
    email = openapi.Parameter(
        'email',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='email',  # 쿼리 설명
        type=openapi.TYPE_STRING
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
            data = request.data
            category_list = data['category_list']
            data['movie_id'] = create_movie(data)

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
        operation_description="이메일 중복 조회",
        operation_id='check existence',
        manual_parameters=[email],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'is_exist': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }))})
    def read(self, request):
        try:
            email = request.GET.get('email')
            result = dict()
            result['is_exist'] = True if Member.objects.filter(email=email, status=STATUS_ACTIVE).count() > 0 else False

            return Response(data=result, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)
