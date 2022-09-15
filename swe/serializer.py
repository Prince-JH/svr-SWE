from django.apps import apps
# from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models import TextField
from rest_framework.fields import Field, CharField, DateTimeField, IntegerField, BooleanField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from swe import (
    models as m,
    signals as sg,
)


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


class Genre(ModelSerializer):
    name: Field = CharField()
    is_valid: Field = BooleanField(read_only=True)
    created_at: Field = DateTimeField(read_only=True)
    deleted_at: Field = DateTimeField(read_only=True)

    class Meta:
        model = m.Genre
        exclude = ('id',)


class MovieGenreAssoc(ModelSerializer):
    movie: Field = SlugRelatedField(
        slug_field='id',
        queryset=apps.get_model('swe', 'Movie').objects.all()
    )
    genre: Field = SlugRelatedField(
        slug_field='id',
        queryset=apps.get_model('swe', 'Genre').objects.all()
    )
    is_valid: Field = BooleanField(read_only=True)
    created_at: Field = DateTimeField(read_only=True)
    deleted_at: Field = DateTimeField(read_only=True)

    class Meta:
        model = m.MovieGenreAssoc
        exclude = ('id',)


class UserProfile(ModelSerializer):
    user: Field = SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all()
    )
    profession: Field = CharField(max_length=100)
    address: Field = CharField(max_length=200)
    age: Field = IntegerField()
    sex: Field = CharField(max_length=20)
    is_valid: Field = BooleanField(read_only=True)
    created_at: Field = DateTimeField(read_only=True)
    deleted_at: Field = DateTimeField(read_only=True)

    class Meta:
        model = m.UserProfile
        exclude = ('id',)

    def create(self, validated_data):
        super().create(validated_data)
        sg.member_created.send(sender=m.UserProfile.__class__, data=validated_data)

