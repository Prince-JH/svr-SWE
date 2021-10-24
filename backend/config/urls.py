"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from swe.views_user import UserSign

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger SWE API",
        default_version="v1",
        description="SWE API 문서",
        contact=openapi.Contact(name="charge", email="aljihoon@ajou.ac.kr")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('swe.urls')),
    # path('swe/v1/login', UserSign.as_view({"post": "create"}), name='user-sign')

]

# 이건 디버그일때만 swagger 문서가 보이도록 해주는 설정이라는 듯. urlpath도 이 안에 설정 가능해서, debug일때만 작동시킬 api도 설정할 수 있음.
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^v1/swe/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                name="schema-json"),
        re_path(r'^v1/swe/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^v1/swe/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), ]
