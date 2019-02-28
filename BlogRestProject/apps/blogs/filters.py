import django_filters
from django.db.models import Q

from .models import BlogsArticle

class BlogsArticleFilter(django_filters.rest_framework.FilterSet):
    """
    文章过滤类
    """
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value))

    class Meta:
        model = BlogsArticle
        fields = ['is_recommend',]
