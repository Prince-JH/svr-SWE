import traceback

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.utils import timezone
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, mixins, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from swe.func import create_member, get_user, token_obtain_pair
from swe.globals import *
from swe.models import Member


class UserSign(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    """
    유저
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
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="회원 가입",
        operation_id='회원 가입',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                'profession': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING, example="서울시 강남구 삼성동"),
                'sex': openapi.Schema(type=openapi.TYPE_STRING, description="M: 남자, W: 여자"),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password_confirm': openapi.Schema(type=openapi.TYPE_STRING)
            }))
    def create(self, request):
        try:
            data = request.data
            if data['password'] == data['password_confirm']:
                data['password'] = make_password(data['password'])
                data['status'] = STATUS_ACTIVE
                user = User.objects.create(
                    username=data['email'],
                    password=data['password']
                )
                data['user'] = user.pk
                create_member(data)
            else:
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

            return Response(status=status.HTTP_201_CREATED)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="로그인, 로그아웃",
        operation_id='로그인, 로그아웃',
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
            authentication_classes = []
            data = request.data
            user = User.objects.get(username=data['email'])
            member = Member.objects.filter(email=data['email'], status=STATUS_ACTIVE)

            if check_password((data['password']), user.password):

                user_info = dict()
                user_info['username'] = data['email']
                user_info['password'] = data['password']

                # tokens = token_obtain_pair(user_info)
                # print("tokens:", tokens)
                access, refresh = token_obtain_pair(user_info)
                print(f"access: {access}, refresh: {refresh}")

                result = dict()
                # token = Token.objects.get_or_create(user=user)[0].key
                result['access'] = access
                result['refresh'] = refresh
                result['role'] = member[0].role
                member.update(
                    refresh_token=refresh,
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
        operation_id='이메일 중복 조회',
        manual_parameters=[email],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'is_exist': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                })})
    def read(self, request):
        try:
            email = request.GET.get('email')
            result = dict()
            result['is_exist'] = True if Member.objects.filter(email=email, status=STATUS_ACTIVE).count() > 0 else False

            return Response(data=result, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserInfo(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    """
    유저 정보
    """
    access_token = openapi.Parameter(
        'access-token',  # 쿼리 이름
        openapi.IN_HEADER,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='ACCESS_TOKEN',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    @swagger_auto_schema(
        operation_description="유저 정보 조회",
        operation_id='유저 정보 조회',
        manual_parameters=[access_token],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'address': openapi.Schema(type=openapi.TYPE_STRING),
                    'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'sex': openapi.Schema(type=openapi.TYPE_STRING),
                    'phone_no': openapi.Schema(type=openapi.TYPE_STRING),
                })})
    def read(self, request):
        try:
            user = get_user(request=request)
            if user is None:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            result = dict()
            result['email'] = user.email
            result['name'] = user.name
            result['address'] = user.address
            result['age'] = user.age
            result['sex'] = user.sex
            result['phone_no'] = user.phone_no

            return Response(data=result, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)