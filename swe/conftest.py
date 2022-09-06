from datetime import datetime

import pytest
from django.utils import timezone

from swe import models as m


@pytest.fixture
def code_dummy_A():
    return m.Code.objects.create(
        code='dummy code A',
        name='dummy name A',
    )


@pytest.fixture
def code_dummy_B():
    return m.Code.objects.create(
        code='dummy code B',
        name='dummy name B',
    )



@pytest.fixture
def movie_dummy():
    return m.Movie.objects.create(
        title='Dummy Movie',
        director='Dummy Director',
        release_date=timezone.now()
    )


@pytest.fixture
def movie_image_dummy(movie_dummy):
    return m.MovieImage.objects.create(
        movie=movie_dummy,
        url='dummy url'
    )
