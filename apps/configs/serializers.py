from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Configs
from interfaces.models import Interfaces
from projects.models import Projects


class InterfacesAnotherSerializer(ModelSerializer):
    project = serializers.StringRelatedField(help_text="项目名称")
    pid = serializers.IntegerField(write_only=True, help_text="项目ID")
    iid = serializers.IntegerField(write_only=True, help_text="接口ID")

    class Meta:
        model = Interfaces
        fields = ("iid", "name", "project", "pid")
        extra_kwargs = {"name": {"read_only": True}, "id": {"write_only": True}}

    def validate_pid(self, value):
        # pid进行校验
        if not Projects.objects.filter(id=value, is_delete=False):
            raise serializers.ValidationError("所选项目不存在")
        return value

    def validate_iid(self, value):
        # 接口id进行校验
        if not Interfaces.objects.filter(id=value, is_delete=False):
            raise serializers.ValidationError("所选接口不存在")
        return value

    def validate(self, attrs):
        # 查看这个项目ID跟接口ID是不是一起的
        if not Interfaces.objects.filter(id=attrs["iid"], project_id=attrs["pid"], is_delete=False):
            raise serializers.ValidationError("项目ID和接口ID信息不对应")
        return attrs


class ConfigSerializer(ModelSerializer):
    interface = InterfacesAnotherSerializer(help_text="项目ID和接口ID")

    class Meta:
        model = Configs
        fields = ("id", "name", "interface", "author","request")
        extra_kwargs = {"request": {"write_only": True}}

    def create(self, validated_data):
        interface_dict = validated_data.pop("interface")
        validated_data["interfaces_id"] = interface_dict["iid"]
        return Configs.objects.create(**validated_data)
