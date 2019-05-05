

from rest_framework import serializers

from users.serializers import UserDetailSerializer

from .models import BlogsTag, BlogsCategory, BlogsArticle, BlogsComment

class BlogsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogsTag
        fields = "__all__"

class BlogsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogsCategory
        fields = "__all__"


class BlogsArticleSerializer(serializers.ModelSerializer):

    category = BlogsCategorySerializer(many=False)
    tag = BlogsTagSerializer(many=True)
    user = UserDetailSerializer(many=False)
    comment_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BlogsArticle
        fields = "__all__"
    def get_comment_count(self, obj):
        count = obj.blogscomment_set.all().count()
        return count



class BlogsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogsComment
        fields = "__all__"

