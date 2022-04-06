from rest_framework import serializers
from .models import DebugTalks


class DebugtalkSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text="项目名称", read_only=True)

    class Meta:
        model = DebugTalks
        fields = ("id", "name", "project","debugtalk")
        read_only_fields = ("name", "project")
        extra_kwargs = {
            "debugtalk": {
                "write_only": True
            }
        }
