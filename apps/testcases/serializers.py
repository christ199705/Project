from rest_framework.serializers import ModelSerializer
from interfaces.models import Interfaces
from .models import Testcases
from rest_framework import serializers
from projects.models import Projects


class InterfacesAnotherSerializer(ModelSerializer):
    project = serializers.StringRelatedField()
    pid = serializers.IntegerField(write_only=True, help_text="项目ID")
    iid = serializers.IntegerField(write_only=True, help_text="接口ID")

    class Meta:
        model = Interfaces
        fields = ("iid", "name", "pid", "project")
        extra_kwargs = {
            "name": {"read_only": True}
        }

    def validate(self, attrs):
        if not Projects.objects.filter(is_delete=False, id=attrs["pid"]):
            raise serializers.ValidationError("项目ID不存在")
        if not Interfaces.objects.filter(is_delete=False, id=attrs["iid"]):
            raise serializers.ValidationError("接口ID不存在")
        if not Interfaces.objects.filter(is_delete=False, id=attrs["iid"], project=attrs["pid"]):
            raise serializers.ValidationError("接口ID和项目ID不对应")
        return attrs


class TestcasesSerializer(ModelSerializer):
    interfaces = InterfacesAnotherSerializer(help_text="所属项目和接口信息")

    class Meta:
        model = Testcases
        fields = ("id", "name", "interfaces", "include", "author", "request")
        extra_kwargs = {
            "include": {
                "write_only": True
            },
            "request": {"write_only": True
                        }

        }

    def create(self, validated_data):
        interface_dict = validated_data.pop("interfaces")
        validated_data["interfaces_id"] = interface_dict["iid"]
        return Testcases.objects.create(**validated_data)
