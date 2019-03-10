
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, help_text='密码', label='密码', write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "name", "avatar", "birthday",
                  "gender", "mobile", "qq", "email", "url", "password")


class UserRegSerializer(serializers.ModelSerializer):

    username = serializers.CharField(label='用户名', help_text='用户名', required=True,
                                     allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')])
    password = serializers.CharField(style={'input_type': 'password'}, help_text='密码', label='密码', write_only=True)

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        return attrs

    class Meta:

        model = User

        fields = ('username', 'mobile', 'password')