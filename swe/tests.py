from rest_framework.test import APIClient
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
import json


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
