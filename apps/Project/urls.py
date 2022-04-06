"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from rest_framework.schemas.views import SchemaView

Schema_view = get_schema_view(
    openapi.Info(
        title="测试开发平台接口文档",
        default_version='v1.0',
        description="秦旺测试开发平台接口文档",
        terms_of_service="http://qinwang.work",
        contact=openapi.Contact(email="qinwang@codemao.cn"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),  权限类
)
urlpatterns = [

    path('project/', include("projects.urls")),
    path('interface/', include("interfaces.urls")),
    path('env/', include("envs.urls")),
    path('debugtalk/', include("debugtalks.urls")),
    path('testsuit/', include("testsuits.urls")),
    path('report/', include("reports.urls")),
    path('config/', include("configs.urls")),
    path('api/', include("rest_framework.urls")),
    path('swagger/', Schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
