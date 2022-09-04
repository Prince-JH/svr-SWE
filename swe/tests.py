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
        print()
        print(code_dummy_A.last_update_date)
        print(code_dummy_B.last_update_date)

        Code.objcets.get(pk=code_dummy_A.pk).save()
        Code.objcets.filter(pk=code_dummy_B.pk).update()
        print(Code.objcets.get(pk=code_dummy_A.pk).last_update_date)
        print(Code.objcets.get(pk=code_dummy_B.pk).last_update_date)
