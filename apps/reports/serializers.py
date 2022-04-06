from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Reports


class ReportSerializer(ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Reports
        exclude = ("update_time", "is_delete")
        extra_kwargs = {
            "html": {
                "write_only": True
            }
        }
