from datetime import datetime

import pytest
from django.utils import timezone

from swe import models as m


@pytest.fixture
def movie_dummy_1():
    return m.Movie.objects.create(
        title='Dummy Movie',
        director='Dummy Director',
        release_date=timezone.now()
    )

@pytest.fixture
def movie_dummy_2():
    return m.Movie.objects.create(
        title='Dummy Movie2',
        director='Dummy Director2',
        release_date=timezone.now()
    )


@pytest.fixture
def movie_image_dummy(movie_dummy_1):
    return m.MovieImage.objects.create(
        movie=movie_dummy_1,
        url='dummy url'
    )


@pytest.fixture
def genre_dummy():
    return m.Genre.objects.create(
        name='dummy genre'
    )


@pytest.fixture
def movie_genre_assoc_dummy(movie_dummy_1, genre_dummy):
    return m.MovieGenreAssoc.objects.create(
        movie=movie_dummy_1,
        genre=genre_dummy
    )
