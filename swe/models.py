import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils import timezone


class LifeCycleModel(models.Model):
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class Code(LifeCycleModel):
    code = models.CharField(db_index=True, max_length=100, default='')
    name = models.CharField(db_index=True, max_length=200, default='')
    description = models.TextField(null=True)
    parent_code = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'code'
        app_label = 'swe'

    def __iter__(self):
        yield 'code_id', self.pk


class Movie(LifeCycleModel):
    title = models.CharField(db_index=True, max_length=200, default='')
    director = models.CharField(db_index=True, max_length=200, default='')
    release_date = models.DateTimeField()
    total_view = models.IntegerField(default=0)
    daily_view = models.IntegerField(default=0)

    class Meta:
        db_table = 'movie'
        app_label = 'swe'

    @property
    def get_title(self):
        "Returns the movie's title."
        if self.release_date < timezone.now():
            return "(개봉)" + self.title
        else:
            return "(미개봉)" + self.title

    def __iter__(self):
        yield 'movie_id', self.pk


class MovieImage(LifeCycleModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='movie_image_meta')
    url = models.TextField(null=True, default=True)

    class Meta:
        db_table = 'movie_image'
        app_label = 'swe'

    def __iter__(self):
        yield 'movie_image_id', self.pk


class MovieMeta(LifeCycleModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='movie_meta')
    type_code = models.CharField(db_index=True, max_length=50, default='')

    class Meta:
        db_table = 'movie_meta'
        app_label = 'swe'

    def __iter__(self):
        yield 'movie_meta_id', self.pk


class Member(LifeCycleModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(db_index=True, max_length=200, default='')
    profession = models.CharField(max_length=50, default='')
    name = models.CharField(max_length=50, default='')
    address = models.TextField(default='')
    age = models.IntegerField(db_index=True, default=0)
    sex = models.CharField(max_length=10, default='')
    refresh_token = models.TextField(default='')
    password = models.TextField(default='')
    phone_no = models.CharField(max_length=50, default='')
    role = models.CharField(max_length=20, default='user')

    class Meta:
        db_table = 'member'
        app_label = 'swe'

    def __iter__(self):
        yield 'member_id', self.pk


class Request(LifeCycleModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='request')
    user = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='user_id',
                             related_name='request')

    class Meta:
        db_table = 'request'
        app_label = 'swe'

    def __iter__(self):
        yield 'request_id', self.pk


class ReOpen(LifeCycleModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='re_open')

    class Meta:
        db_table = 're_open'
        app_label = 'swe'

    def __iter__(self):
        yield 're_open_id', self.pk


class Comment(LifeCycleModel):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, db_column='request_id',
                                related_name='comment', null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='comment')
    user = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='user_id',
                             related_name='comment')
    content = models.TextField(default='')

    class Meta:
        db_table = 'comment'
        app_label = 'swe'

    def __iter__(self):
        yield 'comment_id', self.pk
