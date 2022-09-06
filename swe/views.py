from django.apps import apps

from rest_framework import generics as g
from rest_framework import filters as rf

from swe import serializer as s


class MovieList(g.ListCreateAPIView):
    queryset = apps.get_model('swe', 'Movie').objects.all()
    serializer_class = s.Movie
    filter_backends = [rf.OrderingFilter]
    ordering_field = ['id']
    ordering = ['-id']


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
