from django.apps import apps

from rest_framework import generics as g
from rest_framework import filters as rf
from swe import filters as f

from swe import serializer as s

'''
search_field
'^' : starts-with search
'=' : exact matches
'@' : full-text search
'$' : regax search
'''


class MovieList(g.ListCreateAPIView):
    queryset = apps.get_model('swe', 'Movie').objects.all()
    serializer_class = s.Movie
    filter_backends = [rf.OrderingFilter, rf.SearchFilter, f.IdsFilter]
    ordering_field = ['id']
    ordering = ['-id']
    search_fields = ['title', 'director']


class MovieDetail(g.RetrieveUpdateDestroyAPIView):
    queryset = apps.get_model('swe', 'Movie').objects.all()
    serializer_class = s.Movie
    lookup_field = 'id'


class MovieImageList(g.ListCreateAPIView):
    queryset = apps.get_model('swe', 'MovieImage').objects.all()
    serializer_class = s.MovieImage
    filter_backends = [rf.OrderingFilter]
    ordering_field = ['id']
    ordering = ['-id']


class MovieImageDetail(g.RetrieveUpdateDestroyAPIView):
    queryset = apps.get_model('swe', 'MovieImage').objects.all()
    serializer_class = s.MovieImage
    lookup_field = 'id'


class GenreList(g.ListCreateAPIView):
    queryset = apps.get_model('swe', 'Genre').objects.all()
    serializer_class = s.Genre
    filter_backends = [rf.OrderingFilter]
    ordering_field = ['id']
    ordering = ['-id']


class GenreDetail(g.RetrieveUpdateDestroyAPIView):
    queryset = apps.get_model('swe', 'Genre').objects.all()
    serializer_class = s.Genre
    lookup_field = 'id'


class MovieGenreAssocList(g.ListCreateAPIView):
    queryset = apps.get_model('swe', 'MovieGenreAssoc').objects.all()
    serializer_class = s.MovieGenreAssoc
    filter_backends = [rf.OrderingFilter]
    ordering_field = ['id']
    ordering = ['-id']


class MovieGenreAssocDetail(g.RetrieveUpdateDestroyAPIView):
    queryset = apps.get_model('swe', 'MovieGenreAssoc').objects.all()
    serializer_class = s.MovieGenreAssoc
    lookup_field = 'id'


class UserProfileList(g.ListCreateAPIView):
    queryset = apps.get_model('swe', 'UserProfile').objects.all()
    serializer_class = s.UserProfile
    filter_backends = [f.IdsFilter]