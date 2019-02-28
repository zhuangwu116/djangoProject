
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ("id", "username", "name", "avatar", "birthday",
                  "gender", "mobile", "qq", "email", "url")