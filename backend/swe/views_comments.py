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
    convert_codes_to_name_list, get_user, create_comment
from swe.globals import *
from swe.models import Member, Movie, Code, MovieMeta, Request, Comment


class ViewComment(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    """
    댓글
    """
    access_token = openapi.Parameter(
        'access-token',  # 쿼리 이름
        openapi.IN_HEADER,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='ACCESS_TOKEN',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )
    update_type = openapi.Parameter(
        'update_type',  # 쿼리 이름
        openapi.IN_QUERY,  # IN_QUERY, IN_PATH, IN_BODY, IN_FROM, IN_HEADER
        description='Update or Delete',  # 쿼리 설명
        type=openapi.TYPE_STRING
        # TYPE_STRING, TYPE_NUMBER, TYPE_OBJECT, TYPE_INTEGER, TYPE_BOOLEAN, TYPE_ARRAY, TYPE_FILE
    )

    @swagger_auto_schema(
        operation_description="댓글 등록",
        operation_id='댓글 등록',
        manual_parameters=[access_token],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'movie_id': openapi.Schema(type=openapi.TYPE_STRING),
                'content': openapi.Schema(type=openapi.TYPE_STRING)
            }))
    def create(self, request):
        try:
            user = get_user(request=request)
            with transaction.atomic():
                data = request.data
                data['user'] = user.pk
                data['movie'] = data['movie_id']
                data['status'] = STATUS_ACTIVE
                data['creation_date'] = timezone.now()
                data['last_update_date'] = timezone.now()
                create_comment(data)

            return Response(status=status.HTTP_201_CREATED)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="댓글 수정 및 삭제",
        operation_id='댓글 수정 및 삭제',
        manual_parameters=[access_token, update_type],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING)
            }))
    def update(self, request, comment_id):
        try:
            user = get_user(request=request)
            comment = Comment.objects.filter(id=comment_id)
            update_type = request.query_params.get('update_type', 'Update')
            data = request.data

            if comment[0].user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            with transaction.atomic():
                if update_type == UPDATE_TYPE_UPDATE:
                    comment.update(
                        content=data['content'],
                        last_update_date=timezone.now()
                    )
                else:
                    comment.update(
                        status=STATUS_INACTIVE,
                        end_date=timezone.now(),
                        last_update_date=timezone.now()
                    )

            return Response(status=status.HTTP_200_OK)

        except:
            traceback.print_exc()

            return Response(status=status.HTTP_400_BAD_REQUEST)
