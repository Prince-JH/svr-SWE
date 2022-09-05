
from django.apps import apps
from rest_framework.fields import Field, CharField, DateTimeField, IntegerField, BooleanField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from swe.models import *


class Movie(ModelSerializer):
    title: Field = CharField()
    director: Field = CharField
    release_date: Field = DateTimeField()
    total_view: Field = DateTimeField()
    daily_view: Field = IntegerField(required=False, default=0)
    is_valid: Field = BooleanField(read_only=True)
    created_at: Field = DateTimeField(read_only=True)
    deleted_at: Field = DateTimeField(read_only=True)


    class Meta:
        model = Movie
        exclude = ('id',)
