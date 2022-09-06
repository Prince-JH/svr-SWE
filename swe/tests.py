import pytest
from rest_framework.test import APIClient
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
import json

from swe.models import Code


class TestUtil:
    @pytest.mark.django_db
    def test_difference_between_update_and_save(self, code_dummy_A, code_dummy_B):
        before_A_last_update_date = code_dummy_A.last_update_date
        before_B_last_update_date = code_dummy_B.last_update_date

        # update
        Code.objects.get(pk=code_dummy_A.pk).save()
        Code.objects.filter(pk=code_dummy_B.pk).update()

        after_A_last_update_date = Code.objects.get(pk=code_dummy_A.pk).last_update_date
        after_B_last_update_date = Code.objects.get(pk=code_dummy_B.pk).last_update_date

        assert before_A_last_update_date != after_A_last_update_date
        assert before_B_last_update_date == after_B_last_update_date


class TestViewsMovie:
    @pytest.mark.django_db
    def test_list_should_return_empty_list(self, client):
        response = client.get('/api/movies/')
        assert response.status_code == 200
        assert json.loads(response.content) == []

    @pytest.mark.django_db
    def test_list_should_return_one(self, client, movie_dummy):
        response = client.get('/api/movies/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

        assert movie_dummy.total_view == 0
        assert movie_dummy.daily_view == 0

    @pytest.mark.django_db
    def test_search_a_movie_should_return_one(self, client, movie_dummy):
        response = client.get(f'/api/movies/{movie_dummy.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['title'] == movie_dummy.title


class TestViewsMovieImage:
    @pytest.mark.django_db
    def test_list_should_return_empty_list(self, client):
        response = client.get('/api/movies-images/')
        assert response.status_code == 200
        assert json.loads(response.content) == []

    @pytest.mark.django_db
    def test_list_should_return_one(self, client, movie_dummy, movie_image_dummy):
        response = client.get('/api/movies-images/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

        assert movie_image_dummy.movie == movie_dummy

    @pytest.mark.django_db
    def test_search_a_movie_image_should_return_one(self, client, movie_image_dummy):
        response = client.get(f'/api/movies-images/{movie_image_dummy.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['url'] == movie_image_dummy.url

    @pytest.mark.django_db
    def test_list_by_movie(self, client, movie_dummy, movie_image_dummy):
        response = client.get(f'/api/movies-images/?movie={movie_dummy.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        assert 1 == len(content)
