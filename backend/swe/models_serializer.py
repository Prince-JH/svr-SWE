from rest_framework import serializers

from swe.models import Code, Movie, MovieMeta, Member, Request, Comment, ReOpen


class SerializerCode(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'


class SerializerMovie(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class SerializerMovieMeta(serializers.ModelSerializer):
    class Meta:
        model = MovieMeta
        fields = '__all__'


class SerializerMember(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class SerializerRequest(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class SerializerComment(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class SerializerReOpen(serializers.ModelSerializer):
    class Meta:
        model = ReOpen
        fields = '__all__'
