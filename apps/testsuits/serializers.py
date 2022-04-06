from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Testsuits
from projects.models import Projects


class TestsuitSerializer(ModelSerializer):
    project = serializers.StringRelatedField(label="所属项目")
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), help_text="项目ID")
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Testsuits
        exclude = ("is_delete",)

    def create(self, validated_data):
        project = validated_data.pop("project_id")
        validated_data["project"] = project
        return super().create(validated_data)

    def update(self, instance, validated_data):
        project = validated_data.pop("project_id")
        validated_data["project"] = project
        return super().update(instance, validated_data)
