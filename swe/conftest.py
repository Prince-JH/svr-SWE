from datetime import datetime

import pytest
from django.utils import timezone

from swe import models as m


@pytest.fixture
def code_dummy_A():
    code = m.Code.objects.create(
        code='dummy code A',
        name='dummy name A',
    )
    return code


@pytest.fixture
def code_dummy_B():
    code = m.Code.objects.create(
        code='dummy code B',
        name='dummy name B',
    )
    return code


@pytest.fixture
def movie_dummy():
    code = m.Movie.objects.create(
        title='Dummy Movie',
        director='Dummy Director',
        release_date=timezone.now()
    )
    return code
