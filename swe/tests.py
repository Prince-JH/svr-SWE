import pytest
from rest_framework.test import APIClient
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
import json

from swe.models import Code


class ScheduleAPITests(TestCase):
    databases = '__all__'

    def test_save_teacher_schedule(self):
        client = APIClient()
        url = reverse('user-sign')
        data = {
            "email": "temp@temp.com",
            "name": "temp",
            "age": 25,
            "password": "123",
            "password_confirm": "123"
        }

        response = client.post(url, json.dumps(data), content_type='application/json')
        self.assertEquals(response.status_code, 201)

        response = client.get(url + '?email=temp@temp.com', content_type='application/json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['is_exist'], True)


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