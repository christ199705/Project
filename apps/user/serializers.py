from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(label="确认密码", help_text="确认密码", min_length=6, max_length=20,
                                             error_messages={"min_length": "确认密码最小长度为6位", "max_length": "确认密码最大长度为20位"},
                                             write_only=True)

    # token = serializers.CharField(label="token", help_text="token", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "password_confirm")
        extra_kwargs = {
            # 用户名长度需要重写，之前长度为 150以下
            "username": {
                "label": "用户名", "help_text": "用户名", "min_length": 6, "max_length": 20,
                "error_messages": {"min_length": "用户名最小长度为6位", "max_length": "用户名最大长度为20位"}
            },

            # 默认邮箱可以不穿  "required": True： 必传    ,
            "email": {
                "label": "邮箱", "help_text": "邮箱", "required": True
            },
            "password": {
                "label": "密码", "help_text": "密码", "write_only": True, "min_length": 6, "max_length": 20,
                "error_messages": {"min_length": "密码最小长度为6位", "max_length": "密码最大长度为20位"}
            }

        }

    def validate(self, attrs):
        if attrs["password_confirm"] != attrs["password"]:
            raise serializers.ValidationError({"error_message": "密码和确认密码不一致"})
        return attrs

    def create(self, validated_data):
        del validated_data["password_confirm"]
        # create_user可以返回父类的create方法，自动加密什么，不能使用create
        return User.objects.create_user(**validated_data)
