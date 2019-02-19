
import re

from django.conf import settings

from rest_framework import serializers

from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress

from goods.serializers import GoodsSerializer



class UserFavDetailSerializer(serializers.ModelSerializer):

    goods = GoodsSerializer()

    class Meta:
        model = UserFav

        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d: %H:%M:%S')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d: %H:%M:%S')
    signer_mobile = serializers.CharField(max_length=11)
    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "signer_mobile", "add_time")
    def validate_signer_mobile(self, signer_mobile):
        # 验证手机是否合法
        print(signer_mobile)
        if not re.match(settings.REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号码非法")
        return signer_mobile