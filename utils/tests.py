import pytest

import json

from swe.models import Log


class TestSignal:
    @pytest.mark.django_db
    def test_signal_receiver_should_invoke(self, client):
        assert Log.objects.all().count() == 0
        data = {
            'user': None,
            'profession': 'student',
            'address': 'Suwon',
            'age': 15,
            'sex': 'male'
        }
        response = client.post('/api/user-profiles/', data=data,
                               content_type='application/json')
        assert response.status_code == 201

        assert Log.objects.all().count() == 1