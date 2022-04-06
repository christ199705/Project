from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Envs


class EnvSerializer(ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)

    class Meta:
        model = Envs
        exclude = ("update_time", "is_delete")
