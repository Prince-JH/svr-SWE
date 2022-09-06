from django.apps import apps
from django.db.models import TextField
from rest_framework.fields import Field, CharField, DateTimeField, IntegerField, BooleanField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from swe import models as m


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
        model = m.Movie
        exclude = ('id',)


class MovieImage(ModelSerializer):
    movie: Field = SlugRelatedField(
        slug_field='id',
        queryset=apps.get_model('swe', 'Movie').objects.all()
    )
    url: Field = TextField()
    is_valid: Field = BooleanField(read_only=True)
    created_at: Field = DateTimeField(read_only=True)
    deleted_at: Field = DateTimeField(read_only=True)

    class Meta:
        model = m.MovieImage
        exclude = ('id',)
