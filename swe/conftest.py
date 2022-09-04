from datetime import datetime, timezone

import pytest

from swe.models import Code

@pytest.fixture
def code_dummy_A():
    code = Code.objects.create(
        code='dummy code A',
        name='dummy name A',
    )
    return code


@pytest.fixture
def code_dummy_B():
    code = Code.objects.create(
        code='dummy code B',
        name='dummy name B',
    )
    print('codeB:', code)
    return code
