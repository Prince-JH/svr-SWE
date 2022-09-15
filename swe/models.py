import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class LifeCycleModel(models.Model):
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class Movie(LifeCycleModel):
    title = models.CharField(db_index=True, max_length=100, default='')
    director = models.CharField(db_index=True, max_length=100, default='')
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


class MovieImage(LifeCycleModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='movie_image_meta')
    url = models.TextField(null=True, default=True)

    class Meta:
        db_table = 'movie_image'
        app_label = 'swe'


class Genre(LifeCycleModel):
    name = models.CharField(db_index=True, max_length=50, default='')

    class Meta:
        db_table = 'genre'
        app_label = 'swe'


class MovieGenreAssoc(LifeCycleModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='movie')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, db_column='genre_id',
                              related_name='genre')

    class Meta:
        db_table = 'movie_genre_assoc'
        app_label = 'swe'


class UserProfile(LifeCycleModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=50, default='')
    address = models.TextField(default='')
    age = models.IntegerField(db_index=True, default=0)
    sex = models.CharField(max_length=10, default='')

    class Meta:
        db_table = 'profile'
        app_label = 'swe'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


class Request(LifeCycleModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='request')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id',
                             related_name='request')

    class Meta:
        db_table = 'request'
        app_label = 'swe'


class ReOpen(LifeCycleModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='re_open')

    class Meta:
        db_table = 're_open'
        app_label = 'swe'


class Comment(LifeCycleModel):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, db_column='request_id',
                                related_name='comment', null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id',
                              related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id',
                             related_name='comment')
    content = models.TextField(default='')

    class Meta:
        db_table = 'comment'
        app_label = 'swe'


class Log(models.Model):
    data = models.CharField(max_length=100)
