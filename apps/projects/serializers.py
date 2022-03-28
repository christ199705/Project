from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from projects.models import Projects
from debugtalks.models import DebugTalks
from interfaces.models import Interfaces


class ProjectModelSerializer(ModelSerializer):
    # interface_count = serializers.IntegerField(help_text="用例总数")

    class Meta:
        model = Projects
        exclude = ("update_time", "is_delete")
        extra_kwargs = {
            "create_time": {"read_only": True},
            "interface_count": {"read_only": True},
        }

    def create(self, validated_data):
        project_obj = super().create(validated_data=validated_data)
        DebugTalks.objects.create(project=project_obj)
        return project_obj


class ByInterfacesSerializer(ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ["id", "name"]


class ProjectByInterfacesSerializer(ModelSerializer):
    interface_set = ByInterfacesSerializer(read_only=True, many=True)

    class Meta:
        model = Projects
        fields = ["id", "interface_set"]
