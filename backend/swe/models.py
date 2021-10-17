from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class LifeCycleModel(models.Model):
    status = models.CharField(max_length=20, default='')
    creation_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=50, default='')

    class Meta:
        abstract = True


class Code(LifeCycleModel):
    code = models.CharField(db_index=True, max_length=100, default='')
    name = models.CharField(db_index=True, max_length=200, default='')
    description = models.TextField(null=True)
    parent_code = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'code'
        app_label = 'swe'

    def __iter__(self):
        yield 'code_id', self.pk


class Movie(LifeCycleModel):
    title = models.CharField(db_index=True, max_length=200, default='')
    director = models.CharField(db_index=True, max_length=200, default='')
    release_date = models.DateTimeField()
    poster_path = models.TextField(default='')

    class Meta:
        db_table = 'movie'
        app_label = 'swe'

    def __iter__(self):
        yield 'movie_id', self.pk


class MovieMeta(LifeCycleModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='movie_meta')
    type_code = models.ForeignKey(Code, on_delete=models.CASCADE, db_column='type_code_id',
                                  related_name='movie_meta')

    class Meta:
        db_table = 'movie_meta'
        app_label = 'swe'

    def __iter__(self):
        yield 'movie_meta_id', self.pk


class Member(LifeCycleModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(db_index=True, max_length=200, default='')
    name = models.CharField(max_length=50, default='')
    age = models.IntegerField(db_index=True, default=0)
    access_token = models.TextField(default='')
    password = models.TextField(default='')
    phone_no = models.CharField(max_length=50, default='')

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


class Comment(LifeCycleModel):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, db_column='request_id',
                                related_name='comment')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='comment')
    user = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='user_id',
                             related_name='comment')

    class Meta:
        db_table = 'comment'
        app_label = 'swe'

    def __iter__(self):
        yield 'comment_id', self.pk