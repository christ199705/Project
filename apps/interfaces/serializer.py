from rest_framework.serializers import ModelSerializer
from .models import Interfaces
from rest_framework import serializers
from testcases.models import Testcases
from projects.models import Projects
from configs.models import Configs


class InterfaceSerializer(ModelSerializer):
    project = serializers.StringRelatedField(help_text="项目名称")
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), help_text="项目ID")

    class Meta:
        model = Interfaces
        exclude = ("update_time", "is_delete")

    # 重写create,替换掉我们不需要的字段名 project_id,但是需要他的值
    def create(self, validated_data):
        data = validated_data.pop("project_id")
        validated_data["project"] = data
        return super().create(validated_data)

    # 重写update,替换掉我们不需要的字段名 project_id,但是需要他的值
    def update(self, instance, validated_data):
        data = validated_data.pop("project_id")
        validated_data["project"] = data
        return super().update(instance, validated_data)


class InterfacesTestcasesSerializers(ModelSerializer):
    class Meta:
        model = Testcases
        fields = ["id", "name"]


# class InterfacesTestcasesSerializersTwo(ModelSerializer):
#     testcases_set = InterfacesTestcasesSerializers(read_only=True,many=True)
#
#     class Meta:
#         model = Interfaces
#         fields = ["id", "testcases_set"]

class ConfigsSerializers(ModelSerializer):
    class Meta:
        model = Configs
        fields = ["id", "name"]


class InterfacesConfigsSerializers(ModelSerializer):
    configs = ConfigsSerializers(read_only=True, many=True)

    class Meta:
        model = Interfaces
        fields = ["id", "configs"]
