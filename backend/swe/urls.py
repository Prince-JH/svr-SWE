from django.urls import path

from swe.views import UserSign

urlpatterns = [
    path('swe/v1/user', UserSign.as_view({"post": "create", "put": "update", "get": "read"}), name='user-sign')
]
