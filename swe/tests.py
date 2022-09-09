
import pytest

import json


class TestViewsMovie:
    @pytest.mark.django_db
    def test_list_should_return_empty_list(self, client):
        response = client.get('/api/movies/')
        assert response.status_code == 200
        assert json.loads(response.content) == []

    @pytest.mark.django_db
    def test_list_should_return_one(self, client, movie_dummy_1):
        response = client.get('/api/movies/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

        assert movie_dummy_1.total_view == 0
        assert movie_dummy_1.daily_view == 0

    @pytest.mark.django_db
    def test_search_a_movie_should_return_one(self, client, movie_dummy_1):
        response = client.get(f'/api/movies/{movie_dummy_1.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['title'] == movie_dummy_1.title

    @pytest.mark.django_db
    def test_search_by_movie_ids_should_return_all_matching_movies(self, client, movie_dummy_1, movie_dummy_2):
        response = client.get(f'/api/movies/?ids={movie_dummy_1.pk, movie_dummy_2.pk}')
        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == 2

    @pytest.mark.django_db
    def test_search_by_movie_title_should_return_matching_movie(self, client, movie_dummy_1, movie_dummy_2):
        response = client.get(f'/api/movies/?search={movie_dummy_2.title}')
        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == 1


class TestViewsMovieImage:
    @pytest.mark.django_db
    def test_list_should_return_empty_list(self, client):
        response = client.get('/api/movies/images/')
        assert response.status_code == 200
        assert json.loads(response.content) == []

    @pytest.mark.django_db
    def test_list_should_return_one(self, client, movie_dummy_1, movie_image_dummy):
        response = client.get('/api/movies/images/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

        assert movie_image_dummy.movie == movie_dummy_1

    @pytest.mark.django_db
    def test_search_a_movie_image_should_return_one(self, client, movie_image_dummy):
        response = client.get(f'/api/movies/images/{movie_image_dummy.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['url'] == movie_image_dummy.url

    @pytest.mark.django_db
    def test_list_by_movie(self, client, movie_dummy_1, movie_image_dummy):
        response = client.get(f'/api/movies/images/?movie={movie_dummy_1.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        assert 1 == len(content)


class TestViewsGenre:
    @pytest.mark.django_db
    def test_list_should_return_empty_list(self, client):
        response = client.get('/api/genres/')
        assert response.status_code == 200
        assert json.loads(response.content) == []

    @pytest.mark.django_db
    def test_list_should_return_one(self, client, genre_dummy):
        response = client.get('/api/genres/')
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content) == 1
        assert genre_dummy.name == content[0]['name']

    @pytest.mark.django_db
    def test_search_a_movie_image_should_return_one(self, client, genre_dummy):
        response = client.get(f'/api/genres/{genre_dummy.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        assert content['name'] == genre_dummy.name


class TestViewsMovieGenreAssoc:
    @pytest.mark.django_db
    def test_list_should_return_empty_list(self, client):
        response = client.get('/api/movie-genre-assocs/')
        assert response.status_code == 200
        assert json.loads(response.content) == []

    @pytest.mark.django_db
    def test_list_should_return_one(self, client, movie_genre_assoc_dummy):
        response = client.get('/api/movie-genre-assocs/')
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content) == 1

    @pytest.mark.django_db
    def test_search_a_movie_image_should_return_one(self, client, movie_genre_assoc_dummy):
        response = client.get(f'/api/movie-genre-assocs/{movie_genre_assoc_dummy.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        print('content:', content)

    @pytest.mark.django_db
    def test_list_by_movie(self, client, movie_dummy_1, movie_genre_assoc_dummy):
        response = client.get(f'/api/movie-genre-assocs/?movie={movie_dummy_1.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        assert 1 == len(content)

    @pytest.mark.django_db
    def test_list_by_genre(self, client, genre_dummy, movie_genre_assoc_dummy):
        response = client.get(f'/api/movie-genre-assocs/?genre={genre_dummy.pk}/')

        content = json.loads(response.content)
        assert response.status_code == 200
        assert 1 == len(content)